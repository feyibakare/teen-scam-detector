import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_FILE = "scans.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                message TEXT NOT NULL,
                level TEXT NOT NULL,
                score INTEGER NOT NULL,
                keywords TEXT NOT NULL,
                has_link INTEGER NOT NULL,
                uses_shortener INTEGER NOT NULL,
                bookmarked INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)


def create_user(username, password_hash):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, datetime.now(timezone.utc).isoformat()),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(username):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    return dict(row) if row else None


def save_scan(user_id, message, result):
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO scans
               (user_id, created_at, message, level, score, keywords, has_link, uses_shortener)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
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


def get_history(user_id, limit=50):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM scans WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def toggle_bookmark(user_id, scan_id):
    with get_connection() as conn:
        conn.execute(
            "UPDATE scans SET bookmarked = 1 - bookmarked WHERE id = ? AND user_id = ?",
            (scan_id, user_id),
        )


def delete_scan(user_id, scan_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM scans WHERE id = ? AND user_id = ?", (scan_id, user_id)
        )


def delete_all_scans(user_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM scans WHERE user_id = ?", (user_id,))
