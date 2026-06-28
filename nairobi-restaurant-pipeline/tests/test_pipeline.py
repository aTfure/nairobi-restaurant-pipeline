import os
import sys
from pathlib import Path

import psycopg2
import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "nairobi_pipeline"),
        user=os.getenv("POSTGRES_USER", "nairobi_admin"),
        password=os.getenv("POSTGRES_PASSWORD", "local_dev_password_123"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    try:
        yield conn
    finally:
        conn.close()


def test_database_connection(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)


def test_vision_service_healthcheck():
    response = requests.get("http://localhost:8000/health", timeout=10)
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_mock_enrichment_update(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            ALTER TABLE dishes
            ADD COLUMN IF NOT EXISTS image_confidence FLOAT;
            """
        )
        cursor.execute(
            """
            ALTER TABLE dishes
            ADD COLUMN IF NOT EXISTS nutrition_info JSONB;
            """
        )
        cursor.execute(
            """
            INSERT INTO restaurants (name, city, address, lat, lng, source)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (name, lat, lng) DO NOTHING
            RETURNING id;
            """,
            (
                "QA Mock Restaurant",
                "Nairobi",
                "QA Test Address",
                -1.301,
                36.801,
                "pytest",
            ),
        )
        row = cursor.fetchone()
        if row is not None:
            restaurant_id = row[0]
        else:
            cursor.execute(
                "SELECT id FROM restaurants WHERE name = %s AND lat = %s AND lng = %s LIMIT 1",
                ("QA Mock Restaurant", -1.301, 36.801),
            )
            restaurant_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO dishes (restaurant_id, name, image_url, source)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (
                restaurant_id,
                "QA Mock Dish",
                "https://example.com/menu.jpg",
                "pytest",
            ),
        )
        dish_id = cursor.fetchone()[0]

        cursor.execute(
            """
            UPDATE dishes
            SET image_confidence = 0.95,
                nutrition_info = '{"calories": 300}'::jsonb
            WHERE id = %s;
            """,
            (dish_id,),
        )

        cursor.execute(
            "SELECT image_confidence, nutrition_info FROM dishes WHERE id = %s",
            (dish_id,),
        )
        image_confidence, nutrition_info = cursor.fetchone()

    assert image_confidence == 0.95
    assert nutrition_info == {"calories": 300}
