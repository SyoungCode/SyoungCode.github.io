"""
One-time script: downloads all nine Olist CSVs (the full published dataset)
and loads them into whatever Postgres database DATABASE_URL points at.

Run once, after schema.sql has been applied:
    pip install -r requirements.txt
    $env:DATABASE_URL = "postgresql://...."   # from your Supabase project settings (PowerShell)
    python seed.py

Safe to run again — it replaces each table's contents rather than appending
duplicates. Note: geolocation is ~1 million rows, so this step alone can
take a few minutes over the network — that's expected, not a hang.
"""

import io
import os
import sys
import time

import pandas as pd
import requests
from sqlalchemy import create_engine

# Public, unauthenticated mirrors of the real Olist dataset (originally on
# Kaggle, which needs an account to download from — these are plain GitHub
# repos with the raw files, so this script can fetch them with no credentials).
# Split across two repos because one mirror's order_items file was re-shared
# without its shipping_limit_date column — everything else comes from one place.
_MAIN = "https://raw.githubusercontent.com/erood/interviewqs.com_code_snippets/master/Case_1"
_ITEMS = "https://raw.githubusercontent.com/user2739/ecomm_cohort_rfm_project/main"

SOURCES = {
    "orders": f"{_MAIN}/olist_orders_dataset.csv",
    "order_items": f"{_ITEMS}/olist_order_items_dataset.csv",
    "order_payments": f"{_MAIN}/olist_order_payments_dataset.csv",
    "order_reviews": f"{_MAIN}/olist_order_reviews_dataset.csv",
    "customers": f"{_MAIN}/olist_customers_dataset.csv",
    "products": f"{_MAIN}/olist_products_dataset.csv",
    "sellers": f"{_MAIN}/olist_sellers_dataset.csv",
    "geolocation": f"{_MAIN}/olist_geolocation_dataset.csv",
    "product_category_name_translation": f"{_MAIN}/product_category_name_translation.csv",
}

DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
    "order_payments": [],
    "order_reviews": ["review_creation_date", "review_answer_timestamp"],
    "customers": [],
    "products": [],
    "sellers": [],
    "geolocation": [],
    "product_category_name_translation": [],
}


def download_csv(url, retries=4):
    """Download a CSV with retries — the geolocation file alone is ~60MB,
    large enough that a flaky connection can cut it off partway through."""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            return pd.read_csv(io.BytesIO(resp.content))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print(f"  attempt {attempt}/{retries} failed ({exc}), retrying...")
            time.sleep(2 * attempt)
    raise RuntimeError(f"Could not download {url} after {retries} attempts: {last_error}")


def main():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        sys.exit(
            "DATABASE_URL is not set. Get your connection string from Supabase "
            "(Project Settings -> Connect -> Session pooler) and run:\n"
            '  $env:DATABASE_URL = "postgresql://...."   (PowerShell)\n'
            "then try again."
        )

    engine = create_engine(db_url)

    for table, url in SOURCES.items():
        print(f"Downloading {table}...")
        df = download_csv(url)
        for col in DATE_COLUMNS[table]:
            df[col] = pd.to_datetime(df[col])
        print(f"  {len(df)} rows — loading into '{table}'...")
        df.to_sql(table, engine, if_exists="replace", index=False, method="multi", chunksize=5000)
        print(f"  done.")

    print("\nAll nine tables loaded. Try: SELECT COUNT(*) FROM orders; in Supabase's SQL editor.")


if __name__ == "__main__":
    main()
