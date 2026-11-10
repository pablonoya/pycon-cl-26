import sqlite3
from pathlib import Path

DATABASE = Path("registrations.db")


def execute(query, params=()):
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(query, params)


def create_db():
    execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )""")
