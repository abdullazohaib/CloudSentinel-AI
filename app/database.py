"""SQLite database utilities for CloudSentinel AI."""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "incidents.db"


def get_connection() -> sqlite3.Connection:
    """Create a SQLite database connection."""

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create the incidents table if it does not exist."""

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT NOT NULL UNIQUE,
                service_name TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL,
                description TEXT NOT NULL,
                logs TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()