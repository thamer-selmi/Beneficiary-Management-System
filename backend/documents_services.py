from backend.farmers_services import farmer_collection
import sqlite3

DB_PATH = "backend/database.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_documents_table():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS app_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_setting(key: str, default=None):
    init_documents_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return default
    return row["value"]


def set_setting(key: str, value):
    init_documents_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO app_settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (key, str(value)))
    conn.commit()
    conn.close()


class Documents:
    @staticmethod
    def get_name(cin: str):
        init_documents_table()
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT name
            FROM farmers
            WHERE cin = ?
            LIMIT 1
        """, (str(cin),))
        row = cur.fetchone()
        conn.close()

        if row:
            return ''.join(char for char in str(row["name"]) if not char.isdigit())

        return ""

    @staticmethod
    def for_invoice(cin: str) -> list:
        init_documents_table()

        fields = [
            "counter_number",
            "old_counter",
            "current_counter",
            "consumed",
            "price",
            "total_amount",
            "remaining_payment",
            "outstanding_debt",
            "fixed_fees",
        ]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT counter_number, old_counter, current_counter, consumed, price,
                   total_amount, remaining_payment, outstanding_debt, fixed_fees
            FROM farmers
            WHERE cin = ?
        """, (str(cin),))

        rows = cur.fetchall()
        conn.close()

        data = []
        for row in rows:
            data.append([row[field] for field in fields])

        return data

    @staticmethod
    def for_dafter() -> list:
        init_documents_table()

        fields = [
            "total_amount",
            "price",
            "consumed",
            "current_counter",
            "old_counter",
            "counter_number",
            "cin",
            "name",
        ]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT total_amount, price, consumed, current_counter, old_counter,
                   counter_number, cin, name
            FROM farmers
            ORDER BY name
        """)

        rows = cur.fetchall()
        conn.close()

        data = []
        for row in rows:
            data.append([row[field] for field in fields])

        return data

    @staticmethod
    def get_unique_cins():
        init_documents_table()

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT cin
            FROM farmers
            WHERE cin IS NOT NULL AND cin != ''
        """)
        rows = cur.fetchall()
        conn.close()

        return [str(row["cin"]) for row in rows]

    @staticmethod
    def get_invoice_id():
        init_documents_table()

        current_id = get_setting("invoice_id", 0)
        try:
            current_id = int(current_id)
        except (TypeError, ValueError):
            current_id = 0

        new_id = current_id + 1
        set_setting("invoice_id", new_id)

        return new_id

    @staticmethod
    def get_date():
        init_documents_table()

        from_ = get_setting("period_from", "-")
        to_ = get_setting("period_to", "-")
        return [from_, to_]

    @staticmethod
    def update_date(new_from, new_to):
        try:
            init_documents_table()
            set_setting("period_from", new_from)
            set_setting("period_to", new_to)
            return True
        except Exception as e:
            return str(e)





DB_PATH = "backend/database.db"

def set_db_path(new_path=None):
    global DB_PATH

    if new_path:
        DB_PATH = new_path

    # دائمًا ترجع connection جاهز
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn