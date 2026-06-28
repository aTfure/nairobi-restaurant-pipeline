from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any
from urllib import parse, request

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


OVERPASS_URL = "https://overpass-api.de/api/interpreter"
WESTLANDS_BBOX = "-1.29,36.78,-1.25,36.83"


def fetch_osm_restaurants() -> list[dict[str, Any]]:
    query = f"""
    [out:json][timeout:25];
    (
      node[\"amenity\"=\"restaurant\"]({WESTLANDS_BBOX});
      way[\"amenity\"=\"restaurant\"]({WESTLANDS_BBOX});
      relation[\"amenity\"=\"restaurant\"]({WESTLANDS_BBOX});
    );
    out center;
    """

    payload = parse.urlencode({"data": query}).encode("utf-8")
    req = request.Request(
        OVERPASS_URL,
        data=payload,
        headers={"User-Agent": "nairobi-restaurant-pipeline/1.0"},
        method="POST",
    )

    with request.urlopen(req, timeout=30) as response:
        payload_json = json.load(response)

    restaurants: list[dict[str, Any]] = []
    for element in payload_json.get("elements", []):
        tags = element.get("tags", {}) or {}
        name = tags.get("name") or tags.get("brand") or tags.get("operator")
        if not name:
            continue

        lat = element.get("lat")
        lng = element.get("lon")
        if lat is None and element.get("center") is not None:
            lat = element["center"].get("lat")
            lng = element["center"].get("lon")

        if lat is None or lng is None:
            continue

        address_parts = [
            tags.get("addr:street"),
            tags.get("addr:building"),
            tags.get("addr:suburb"),
        ]
        address = ", ".join(part for part in address_parts if part)

        restaurants.append(
            {
                "name": name,
                "city": "Nairobi",
                "address": address or None,
                "lat": float(lat),
                "lng": float(lng),
                "source": "OSM",
            }
        )

    print(f"discovered_restaurants={len(restaurants)}")
    return restaurants


def ingest_osm_restaurants(**context: Any) -> None:
    restaurants = context["ti"].xcom_pull(task_ids="fetch_osm_restaurants") or []
    if not restaurants:
        print("no_restaurants_to_ingest")
        return

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "nairobi_pipeline"),
        user=os.getenv("POSTGRES_USER", "nairobi_admin"),
        password=os.getenv("POSTGRES_PASSWORD", "local_dev_password_123"),
        host=os.getenv("POSTGRES_HOST", "nairobi_db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_restaurants_name_lat_lng_unique
                ON restaurants (name, lat, lng);
                """
            )

            for restaurant in restaurants:
                cursor.execute(
                    """
                    INSERT INTO restaurants (name, city, address, lat, lng, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name, lat, lng) DO UPDATE SET
                        city = EXCLUDED.city,
                        address = EXCLUDED.address,
                        source = EXCLUDED.source;
                    """,
                    (
                        restaurant["name"],
                        restaurant["city"],
                        restaurant["address"],
                        restaurant["lat"],
                        restaurant["lng"],
                        restaurant["source"],
                    ),
                )

        conn.commit()
        print(f"ingested_restaurants={len(restaurants)}")
    finally:
        conn.close()


with DAG(
    dag_id="02_osm_discovery_westlands",
    default_args=DEFAULT_ARGS,
    description="Fetch restaurants from OpenStreetMap for Westlands and ingest them idempotently",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["discovery", "osm", "westlands"],
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_osm_restaurants",
        python_callable=fetch_osm_restaurants,
        dag=dag,
    )

    ingest_task = PythonOperator(
        task_id="ingest_osm_restaurants",
        python_callable=ingest_osm_restaurants,
        dag=dag,
    )

    fetch_task >> ingest_task
