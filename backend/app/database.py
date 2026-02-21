"""
SQLite-backed analysis audit trail.

Tables:
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
            CREATE TABLE IF NOT EXISTS analysis_history (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name  TEXT,
                filename      TEXT NOT NULL,
                tumor_type    TEXT,
                confidence    TEXT,
                region        TEXT,
                grade         TEXT,
                analysis_json TEXT,
                created_at    TEXT NOT NULL
            )
            """
        )
    logger.info("Database initialised at %s", DATABASE_PATH)


# ── Analysis history helpers ────────────────────────────────────────

def log_analysis(
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
                (patient_name, filename, tumor_type, confidence,
                 region, grade, analysis_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (patient_name, filename, tumor_type, confidence,
             region, grade, analysis_json, now),
        )


def get_history(limit: int = 100) -> list[dict]:
    """Retrieve analysis history."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM analysis_history ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]
