"""SQLite storage for private custom-order enquiries."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent / "data" / "orders.sqlite3"
ORDER_STATUSES = ("New", "Contacted", "In Design", "Completed")


def get_connection(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    """Open a connection and ensure the order table exists."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """CREATE TABLE IF NOT EXISTS custom_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            city TEXT NOT NULL,
            category TEXT,
            product TEXT NOT NULL,
            recipient_name TEXT,
            occasion TEXT,
            required_text TEXT,
            budget TEXT,
            preferred_colours TEXT,
            required_date TEXT,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'New'
                CHECK(status IN ('New', 'Contacted', 'In Design', 'Completed')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    # Add fields introduced after the first local version without losing orders.
    columns = {row["name"] for row in connection.execute("PRAGMA table_info(custom_orders)")}
    for name in ("category", "recipient_name", "required_text"):
        if name not in columns:
            connection.execute(f"ALTER TABLE custom_orders ADD COLUMN {name} TEXT")
    connection.commit()
    return connection


def validate_order(order: dict[str, Any]) -> list[str]:
    """Return field errors for required fields and basic email/phone checks."""
    errors: list[str] = []
    required = {
        "customer_name": "Name",
        "phone": "Phone",
        "city": "City",
        "product": "Product",
    }
    for key, label in required.items():
        if not str(order.get(key, "")).strip():
            errors.append(f"{label} is required.")
    phone = re.sub(r"[\s()+-]", "", str(order.get("phone", "")))
    if order.get("phone") and (not phone.isdigit() or not 7 <= len(phone) <= 15):
        errors.append("Enter a valid phone number (7 to 15 digits).")
    email = str(order.get("email", "")).strip()
    if email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        errors.append("Enter a valid email address.")
    return errors


def save_order(order: dict[str, Any], db_path: str | Path = DB_PATH) -> int:
    """Validate and save an order; return its private database ID."""
    errors = validate_order(order)
    if errors:
        raise ValueError(" ".join(errors))
    fields = (
        "customer_name", "phone", "email", "city", "category", "product",
        "recipient_name", "occasion", "required_text", "budget", "preferred_colours",
        "required_date", "notes",
    )
    values = [str(order.get(field, "")).strip() or None for field in fields]
    connection = get_connection(db_path)
    try:
        cursor = connection.execute(
            f"INSERT INTO custom_orders ({', '.join(fields)}) VALUES ({', '.join('?' for _ in fields)})",
            values,
        )
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()
