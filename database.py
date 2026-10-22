
import sqlite3

DB_NAME = "intellishield.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            channel TEXT NOT NULL,
            requests_in_window INTEGER,
            prediction TEXT,
            anomaly_score REAL,
            decision TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def log_request(
    account_id,
    channel,
    requests_in_window,
    prediction,
    anomaly_score,
    decision
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO request_logs (
            account_id,
            channel,
            requests_in_window,
            prediction,
            anomaly_score,
            decision
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        account_id,
        channel,
        requests_in_window,
        prediction,
        anomaly_score,
        decision
    ))

    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM request_logs
        ORDER BY id DESC
    """)

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
