import sqlite3
from datetime import datetime

DB_NAME = "/tmp/intellishield.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            endpoint TEXT,
            request_rate REAL,
            user_agent_score REAL,
            ml_prediction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_decision(ip_address, endpoint, request_rate, user_agent_score, ml_prediction):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO traffic_logs (ip_address, endpoint, request_rate, user_agent_score, ml_prediction)
        VALUES (?, ?, ?, ?, ?)
    """, (ip_address, endpoint, request_rate, user_agent_score, ml_prediction))
    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM traffic_logs")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as blocked FROM traffic_logs WHERE ml_prediction = 'Blocked'")
    blocked = cursor.fetchone()["blocked"]

    cursor.execute("SELECT COUNT(*) as allowed FROM traffic_logs WHERE ml_prediction = 'Allowed'")
    allowed = cursor.fetchone()["allowed"]

    cursor.execute("SELECT * FROM traffic_logs ORDER BY timestamp DESC LIMIT 20")
    recent = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "total_requests": total,
        "blocked": blocked,
        "allowed": allowed,
        "recent_attacks": recent
    }
