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


def verify_restaurant_count() -> None:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "nairobi_pipeline"),
        user=os.getenv("POSTGRES_USER", "nairobi_admin"),
        password=os.getenv("POSTGRES_PASSWORD", "local_dev_password_123"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
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
