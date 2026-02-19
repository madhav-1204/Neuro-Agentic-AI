"""
SQLite-backed user store and analysis audit trail.

Tables:
  users           – Google-authenticated users
  analysis_history – log of every scan analysed (patient history / audit)
"""

import os
import sqlite3
import json
import logging
from datetime import datetime, timezone
from contextlib import contextmanager

from app.config.settings import DATABASE_PATH

logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_db():
    """Yields a sqlite3 connection; commits on success, rolls back on error."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email       TEXT PRIMARY KEY,
                name        TEXT,
                picture     TEXT,
                created_at  TEXT NOT NULL,
                last_login  TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email    TEXT,
                patient_name  TEXT,
                filename      TEXT NOT NULL,
                tumor_type    TEXT,
                confidence    TEXT,
                region        TEXT,
                grade         TEXT,
                analysis_json TEXT,
                created_at    TEXT NOT NULL,
                FOREIGN KEY (user_email) REFERENCES users(email)
            )
            """
        )
    logger.info("Database initialised at %s", DATABASE_PATH)


# ── User helpers ────────────────────────────────────────────────────

def upsert_user(email: str, name: str, picture: str) -> dict:
    """Insert or update a user, returning the user dict."""
    now = _now_iso()
    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE users SET name=?, picture=?, last_login=? WHERE email=?",
                (name, picture, now, email),
            )
        else:
            conn.execute(
                "INSERT INTO users (email, name, picture, created_at, last_login) VALUES (?,?,?,?,?)",
                (email, name, picture, now, now),
            )
    return {"email": email, "name": name, "picture": picture}


def get_user(email: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if row:
            return dict(row)
    return None


# ── Analysis history helpers ────────────────────────────────────────

def log_analysis(
    user_email: str | None,
    patient_name: str,
    filename: str,
    analysis: dict,
):
    """Record an analysis to the audit trail."""
    now = _now_iso()
    tumor_type = analysis.get("tumorType", "")
    confidence = analysis.get("confidence", "")
    region = analysis.get("region", "")
    grade = analysis.get("grade", "")
    analysis_json = json.dumps(analysis)

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO analysis_history
                (user_email, patient_name, filename, tumor_type, confidence,
                 region, grade, analysis_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_email, patient_name, filename, tumor_type, confidence,
             region, grade, analysis_json, now),
        )


def get_history(user_email: str | None = None, limit: int = 100) -> list[dict]:
    """Retrieve analysis history, optionally filtered by user."""
    with get_db() as conn:
        if user_email:
            rows = conn.execute(
                "SELECT * FROM analysis_history WHERE user_email = ? ORDER BY created_at DESC LIMIT ?",
                (user_email, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM analysis_history ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
    return [dict(r) for r in rows]
