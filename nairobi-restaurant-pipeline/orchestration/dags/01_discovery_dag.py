from __future__ import annotations

import os
from datetime import datetime, timedelta

import psycopg2
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


def get_postgres_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "nairobi_db"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        dbname=os.environ.get("POSTGRES_DB"),
    )


def verify_restaurant_count() -> None:
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM restaurants;")
            count = cursor.fetchone()[0]
        conn.commit()
        print(f"restaurants_count={count}")
    finally:
        conn.close()


with DAG(
    dag_id="01_discovery_dag",
    default_args=DEFAULT_ARGS,
    description="Verify the PostgreSQL connection for the discovery layer",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["discovery", "postgres"],
) as dag:
    verify_connection = PythonOperator(
        task_id="verify_connection",
        python_callable=verify_restaurant_count,
        retries=0,
        dag=dag,
    )

    verify_connection
