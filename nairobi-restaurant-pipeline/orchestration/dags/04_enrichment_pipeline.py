from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any

import psycopg2
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


DEFAULT_ARGS = {
    "owner": "nairobi",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


VISION_SERVICE_URL = "http://vision-service:8000/analyze"


def get_postgres_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "nairobi_pipeline"),
        user=os.getenv("POSTGRES_USER", "nairobi_admin"),
        password=os.getenv("POSTGRES_PASSWORD", "local_dev_password_123"),
        host=os.getenv("POSTGRES_HOST", "nairobi_db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def fetch_unprocessed_dishes() -> list[dict[str, Any]]:
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, image_url
                FROM dishes
                WHERE image_url IS NOT NULL
                  AND image_confidence IS NULL
                ORDER BY created_at ASC;
                """
            )
            rows = cursor.fetchall()

        dishes = [
            {"id": row[0], "image_url": row[1]} for row in rows if row[1]
        ]
        print(f"unprocessed_dishes={len(dishes)}")
        return dishes
    finally:
        conn.close()


def enrich_dishes(**context: Any) -> None:
    dishes = context["ti"].xcom_pull(task_ids="fetch_unprocessed_dishes") or []
    if not dishes:
        print("no_unprocessed_dishes_found")
        return

    conn = get_postgres_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                ALTER TABLE dishes
                ADD COLUMN IF NOT EXISTS nutrition_info JSONB;
                """
            )

            processed_count = 0
            for dish in dishes:
                dish_id = dish["id"]
                image_url = dish["image_url"].strip()
                if not image_url:
                    continue

                response = requests.post(
                    VISION_SERVICE_URL,
                    json={"image_url": image_url},
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()

                image_confidence = result.get("image_confidence")
                nutrition_info = result.get("nutrition_info")

                if image_confidence is None:
                    image_confidence = float(result.get("confidence", 0))

                cursor.execute(
                    """
                    UPDATE dishes
                    SET image_confidence = %s,
                        nutrition_info = %s,
                        source = COALESCE(source, 'vision-enriched')
                    WHERE id = %s;
                    """,
                    (
                        image_confidence,
                        json.dumps(nutrition_info) if nutrition_info is not None else None,
                        dish_id,
                    ),
                )
                processed_count += 1
                print(f"processed_dish={dish_id} image_url={image_url}")

        conn.commit()
        print(f"enriched_dishes={processed_count}")
    finally:
        conn.close()


with DAG(
    dag_id="04_enrichment_pipeline",
    default_args=DEFAULT_ARGS,
    description="Enrich dish images by invoking the vision service and storing results idempotently.",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["enrichment", "vision", "dishes"],
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_unprocessed_dishes",
        python_callable=fetch_unprocessed_dishes,
    )

    enrich_task = PythonOperator(
        task_id="enrich_dishes",
        python_callable=enrich_dishes,
        provide_context=True,
    )

    fetch_task >> enrich_task
