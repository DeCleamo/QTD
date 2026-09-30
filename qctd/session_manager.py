"""
Session Management & Replay Detection
SQLite-backed registry of verified signatures.
"""

import sqlite3
import time
from .config import DATABASE_PATH


class SessionManager:
    """
    Tracks every verification attempt in an SQLite database.
    Primary purpose: detect **replay attacks** by recognising duplicate
    signature IDs.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path or DATABASE_PATH
        self._init_db()

    # ── schema ────────────────────────────────────────────────────────

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS verification_log (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    signature_id  TEXT    NOT NULL,
                    signer_id     TEXT,
                    timestamp     REAL    NOT NULL,
                    verdict       TEXT    NOT NULL,
                    error_rate    REAL,
                    threat_type   TEXT,
                    message_hash  TEXT,
                    details       TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sig_id
                ON verification_log(signature_id)
            """)

    # ── replay detection ──────────────────────────────────────────────

    def check_replay(self, signature_id: str) -> bool:
        """Return True if *signature_id* has already been verified."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM verification_log WHERE signature_id = ?",
                (signature_id,),
            ).fetchone()
        return row[0] > 0

    # ── logging ───────────────────────────────────────────────────────

    def log_verification(self, signature_id, signer_id, verdict,
                          error_rate, threat_type=None,
                          message_hash=None, details=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO verification_log
                    (signature_id, signer_id, timestamp, verdict,
                     error_rate, threat_type, message_hash, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (signature_id, signer_id, time.time(), verdict,
                  error_rate, threat_type, message_hash, details))

    # ── queries ───────────────────────────────────────────────────────

    def get_history(self, limit=50):
        """Return the most recent *limit* verification records."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM verification_log ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def clear_history(self):
        """Delete all records (for testing / demo resets)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM verification_log")
