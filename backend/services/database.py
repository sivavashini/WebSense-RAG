import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from services.config import settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    situation TEXT NOT NULL,
    response TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    category TEXT NOT NULL,
    confidence REAL NOT NULL,
    evidence TEXT NOT NULL,
    actions TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    chunks INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
"""


async def init_db() -> None:
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(settings.db_path) as conn:
        conn.executescript(SCHEMA)


def add_incident(payload: dict[str, Any]) -> int:
    with sqlite3.connect(settings.db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO incidents
            (situation, response, risk_level, category, confidence, evidence, actions, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["situation"],
                payload["response"],
                payload["risk_level"],
                payload["category"],
                payload["confidence"],
                json.dumps(payload["evidence"]),
                json.dumps(payload["actions"]),
                datetime.utcnow().isoformat(),
            ),
        )
        return int(cur.lastrowid)


def list_incidents(limit: int = 50) -> list[dict[str, Any]]:
    with sqlite3.connect(settings.db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [
        {
            **dict(row),
            "evidence": json.loads(row["evidence"]),
            "actions": json.loads(row["actions"]),
        }
        for row in rows
    ]


def add_document(filename: str, chunks: int) -> None:
    with sqlite3.connect(settings.db_path) as conn:
        conn.execute(
            "INSERT INTO documents (filename, chunks, created_at) VALUES (?, ?, ?)",
            (filename, chunks, datetime.utcnow().isoformat()),
        )


def stats() -> dict[str, int]:
    with sqlite3.connect(settings.db_path) as conn:
        incidents = conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
        documents = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        chunks = conn.execute("SELECT COALESCE(SUM(chunks), 0) FROM documents").fetchone()[0]
    return {"incidents": incidents, "documents": documents, "chunks": chunks}
