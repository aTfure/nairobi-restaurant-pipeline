from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


DEFAULT_ARGS = {
    "owner": "nairobi",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}


with DAG(
    dag_id="03_acquisition_test",
    default_args=DEFAULT_ARGS,
    description="Exercise the acquisition scraper from Airflow",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["acquisition", "puppeteer"],
) as dag:
    run_scraper = BashOperator(
        task_id="run_scraper",
        bash_command="node /opt/airflow/acquisition/scraper.js https://example.com",
        dag=dag,
    )

    run_scraper
