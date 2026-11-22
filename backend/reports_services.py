from datetime import datetime
import sqlite3

DB_PATH = "backend/database.db"

reports_collection = "reports"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_reports_table():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,              -- activity / payment / counter
        message TEXT,
        cin TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


class Reports:

    @staticmethod
    def addActivityReport(msg, name, cin, counter_number):
        init_reports_table()

        msg = msg.replace("?", "{}").format(name, cin, counter_number)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reports (type, message, cin, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            "activity",
            msg,
            cin,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def addPaymentReport(msg, amount, name, cin, counter_number):
        init_reports_table()

        msg = msg.replace("?", "{}").format(amount, name, cin, counter_number)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reports (type, message, cin, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            "payment",
            msg,
            cin,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def addcounterReport(msg, new_counter, name, cin, counter_number):
        init_reports_table()

        msg = msg.replace("?", "{}").format(new_counter, name, cin, counter_number)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reports (type, message, cin, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            "counter",
            msg,
            cin,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_last_reports(limit=20):
        init_reports_table()

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT message
            FROM reports
            ORDER BY datetime(created_at) DESC
            LIMIT ?
        """, (limit,))

        rows = cur.fetchall()
        conn.close()

        return [row["message"] for row in rows]