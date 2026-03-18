"""
Dagster passes asset values between dependent assets using the configured I/O manager.
In this project, the default filesystem I/O manager stores materialized asset data so downstream
assets like cleaned_orders can load upstream results automatically.
"""

import csv
from dagster import asset


@asset
def raw_orders() -> list[dict]:
    with open("data/orders.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


@asset
def cleaned_orders(raw_orders: list[dict]) -> list[dict]:
    valid_statuses = {"pending", "shipped", "delivered", "cancelled"}
    cleaned = []

    for row in raw_orders:
        required_fields = [
            "order_id",
            "customer_id",
            "product_id",
            "quantity",
            "price",
            "order_date",
            "status",
        ]

        if any(not row.get(field, "").strip() for field in required_fields):
            continue

        status = row["status"].strip().lower()

        if status not in valid_statuses:
            continue

        cleaned_row = {
            "order_id": int(row["order_id"]),
            "customer_id": int(row["customer_id"]),
            "product_id": int(row["product_id"]),
            "quantity": int(row["quantity"]),
            "price": float(row["price"]),
            "order_date": row["order_date"],
            "timestamp": row.get("timestamp", ""),
            "status": status,
        }

        cleaned.append(cleaned_row)

    return cleaned
