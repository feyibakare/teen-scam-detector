import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_FILE = "scans.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                message TEXT NOT NULL,
                level TEXT NOT NULL,
                score INTEGER NOT NULL,
                keywords TEXT NOT NULL,
                has_link INTEGER NOT NULL,
                uses_shortener INTEGER NOT NULL,
                bookmarked INTEGER NOT NULL DEFAULT 0
            )
        """)


def save_scan(message, result):
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO scans
               (created_at, message, level, score, keywords, has_link, uses_shortener)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                message,
                result.level,
                result.score,
                json.dumps(result.keywords),
                int(bool(result.links)),
                int(result.uses_shortener),
            ),
        )
        return cursor.lastrowid


def get_history(limit=50):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM scans ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]

def toggle_bookmark(scan_id):
    with get_connection() as conn:
        conn.execute(
            "UPDATE scans SET bookmarked = 1 - bookmarked WHERE id = ?", (scan_id,)
        )


def delete_scan(scan_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM scans WHERE id = ?", (scan_id,))


def delete_all_scans():
    with get_connection() as conn:
        conn.execute("DELETE FROM scans")