from datetime import datetime
import sqlite3
from backend.reports_services import Reports

DB_PATH = "backend/database.db"

farmer_collection = "farmers"
reports_collection = "reports"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cin TEXT NOT NULL,
        counter_number TEXT NOT NULL,
        old_counter REAL NOT NULL,
        current_counter REAL NOT NULL,
        consumed REAL NOT NULL,
        price REAL NOT NULL,
        total_amount REAL NOT NULL,
        remaining_payment REAL NOT NULL,
        outstanding_debt REAL NOT NULL,
        fixed_fees REAL NOT NULL,
        required_amount REAL NOT NULL,
        entry_date TEXT NOT NULL,
        last_update TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_farmers_cin_counter
    ON farmers(cin, counter_number)
    """)

    conn.commit()
    conn.close()


class Farmers:
    @staticmethod
    def _row_to_dict(row):
        d = dict(row)
        d["_id"] = d["id"]
        return d

    @staticmethod
    def add(
        name: str,
        cin: str,
        counter_number: str,
        old_counter: float,
        current_counter: float,
        price: float,
        payment: float,
        outstanding_debt: float,
        fixed_fees: float,
    ):
        init_db()

        consumed = float(current_counter - old_counter)
        total_amount = float(consumed * price)

        debt = 0.0
        if (payment - total_amount) >= 0:
            payment -= total_amount
        else:
            debt += (total_amount - payment)
            payment = 0.0

        # تسديد الديون المخلدة إن وُجد مبلغ
        if outstanding_debt > 0.0:
            if (payment - outstanding_debt) >= 0:
                payment -= outstanding_debt
            else:
                debt += outstanding_debt
                payment = 0.0

        required_amount = float(debt + fixed_fees)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO farmers (
                name, cin, counter_number,
                old_counter, current_counter, consumed,
                price, total_amount, remaining_payment,
                outstanding_debt, fixed_fees, required_amount,
                entry_date, last_update, password
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, cin, counter_number,
            round(old_counter, 2), round(current_counter, 2), round(consumed, 2),
            price, round(total_amount, 2), round(payment, 2),
            round(debt, 2), round(fixed_fees, 2), round(required_amount, 2),
            datetime.now().strftime("%Y-%m-%d"),
            "غير محدد",
            cin
        ))
        conn.commit()
        conn.close()

        msg = " تمت إضافة '?' صاحب بطاقة تعريف عدد ? إلى النظام ?"
        Reports.addActivityReport(msg, name, cin, counter_number)

    @staticmethod
    def deleteOne(name: str, cin: str, counter_number: str):
        init_db()

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM farmers
            WHERE cin = ? AND counter_number = ?
        """, (str(cin), str(counter_number)))

        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()

        if deleted:
            msg = "تمت حذف '?' صاحب بطاقة تعريف عدد ? من النظام ?"
            Reports.addActivityReport(msg, name, cin, counter_number)
            return True

        return False

    @staticmethod
    def deleteAll():
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM farmers")
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def getAll():
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM farmers")
        rows = cur.fetchall()
        conn.close()
        return [Farmers._row_to_dict(row) for row in rows]

    @staticmethod
    def search(term: str):
        init_db()
        term = term.strip()
        results = []
        is_cin = len(term) == 8 and term.isdigit() and term[0] in ("0", "1")

        conn = get_conn()
        cur = conn.cursor()

        if is_cin:
            cur.execute("SELECT * FROM farmers WHERE cin = ?", (term,))
            rows = cur.fetchall()
            results = [Farmers._row_to_dict(r) for r in rows]

        if not results:
            like_term = f"%{term.lower()}%"
            cur.execute("""
                SELECT * FROM farmers
                WHERE LOWER(name) LIKE ?
                   OR LOWER(counter_number) LIKE ?
            """, (like_term, like_term))
            rows = cur.fetchall()
            results = [Farmers._row_to_dict(r) for r in rows]

        conn.close()
        return results

    @staticmethod
    def get_total_data():
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                COALESCE(SUM(consumed), 0) AS total_consumed,
                COALESCE(SUM(total_amount), 0) AS total_total_amount,
                COALESCE(SUM(outstanding_debt), 0) AS total_debts,
                COALESCE(SUM(fixed_fees), 0) AS total_fees,
                COALESCE(SUM(required_amount), 0) AS total_required_amount
            FROM farmers
        """)
        row = cur.fetchone()
        conn.close()

        return [
            "{:.2f}".format(row["total_consumed"] or 0),
            "{:.2f}".format(row["total_total_amount"] or 0),
            "{:.2f}".format(row["total_debts"] or 0),
            "{:.2f}".format(row["total_fees"] or 0),
            "{:.2f}".format(row["total_required_amount"] or 0),
        ]
    
    @staticmethod
    def for_daftr():
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                COALESCE(SUM(consumed), 0) AS total_consumed,
                COALESCE(SUM(total_amount), 0) AS total_total_amount
            FROM farmers
        """)
        row = cur.fetchone()
        conn.close()

        return [
            "{:.2f}".format(row["total_consumed"] or 0),
            "{:.2f}".format(row["total_total_amount"] or 0),
        ]

    @staticmethod
    def update_payments(
        name: str,
        cin: str,
        counter_number: str,
        new_payment: float,
    ):
        init_db()
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM farmers
            WHERE cin = ? AND counter_number = ?
            LIMIT 1
        """, (str(cin), str(counter_number)))
        row = cur.fetchone()

        if not row:
            conn.close()
            return False

        data = dict(row)
        outstanding_debt = float(data.get("outstanding_debt", 0))
        remaining_payment = float(data.get("remaining_payment", 0))
        fixed_fees = float(data.get("fixed_fees", 0))

        amount = new_payment
        new_payment += remaining_payment

        if new_payment >= outstanding_debt:
            new_payment -= outstanding_debt
            outstanding_debt = 0.0
        else:
            outstanding_debt -= new_payment
            new_payment = 0.0

        required_amount = outstanding_debt + fixed_fees

        cur.execute("""
            UPDATE farmers
            SET outstanding_debt = ?,
                remaining_payment = ?,
                required_amount = ?,
                last_update = ?
            WHERE id = ?
        """, (
            round(outstanding_debt, 2),
            round(new_payment, 2),
            round(required_amount, 2),
            datetime.now().strftime("%Y-%m-%d"),
            data["id"]
        ))

        conn.commit()
        conn.close()

        msg = "تم اضافة مبلغ ? الى ? صاحب رقم البطاقة عدد ? ?"
        Reports.addPaymentReport(msg, amount, name, cin, counter_number)
        return True

    @staticmethod
    def update_fees(
        name: str,
        cin: str,
        counter_number: str,
        payment_for_fees: float,
    ):
        init_db()
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM farmers
            WHERE cin = ? AND counter_number = ?
            LIMIT 1
        """, (str(cin), str(counter_number)))
        row = cur.fetchone()

        if not row:
            conn.close()
            return False

        data = dict(row)
        amount = payment_for_fees

        fixed_fees = float(data.get("fixed_fees", 0))
        remaining_payment = float(data.get("remaining_payment", 0))
        outstanding_debt = float(data.get("outstanding_debt", 0))

        if payment_for_fees >= fixed_fees:
            payment_for_fees -= fixed_fees
            remaining_payment += payment_for_fees
            fixed_fees = 0.0
        else:
            fixed_fees -= payment_for_fees

        required_amount = outstanding_debt + fixed_fees

        cur.execute("""
            UPDATE farmers
            SET remaining_payment = ?,
                fixed_fees = ?,
                required_amount = ?,
                last_update = ?
            WHERE id = ?
        """, (
            round(remaining_payment, 2),
            round(fixed_fees, 2),
            round(required_amount, 2),
            datetime.now().strftime("%Y-%m-%d"),
            data["id"]
        ))

        conn.commit()
        conn.close()

        msg = "تم اضافة مبلغ ? الى ? صاحب رقم البطاقة عدد ? ?"
        Reports.addPaymentReport(msg, amount, name, cin, counter_number)
        return True

    @staticmethod
    def add_fees(
        name: str,
        cin: str,
        counter_number: str,
        fees_amount: float,
    ):
        init_db()
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM farmers
            WHERE cin = ? AND counter_number = ?
            LIMIT 1
        """, (str(cin), str(counter_number)))
        row = cur.fetchone()

        if not row:
            conn.close()
            return False

        data = dict(row)
        fixed_fees = float(data.get("fixed_fees", 0))
        required_amount = float(data.get("required_amount", 0))

        fixed_fees += fees_amount
        required_amount += fees_amount

        cur.execute("""
            UPDATE farmers
            SET fixed_fees = ?,
                required_amount = ?,
                last_update = ?
            WHERE id = ?
        """, (
            round(fixed_fees, 2),
            round(required_amount, 2),
            datetime.now().strftime("%Y-%m-%d"),
            data["id"]
        ))

        conn.commit()
        conn.close()

        msg = "تم اضافة معاليم قارة ? الى ? صاحب رقم البطاقة عدد ? ?"
        Reports.addPaymentReport(msg, fees_amount, name, cin, counter_number)
        return True

    @staticmethod
    def add_new_counter(
        name: str,
        cin: str,
        counter_number: str,
        new_counter: float,
    ):
        init_db()
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM farmers
            WHERE cin = ? AND counter_number = ?
            LIMIT 1
        """, (str(cin), str(counter_number)))
        row = cur.fetchone()

        if not row:
            conn.close()
            return False

        data = dict(row)
        current_counter = float(data.get("current_counter", 0))

        if new_counter < current_counter:
            conn.close()
            return False

        consumed = new_counter - current_counter
        price = float(data.get("price", 0))
        total_amount = consumed * price

        fixed_fees = float(data.get("fixed_fees", 0))
        remaining_payment = float(data.get("remaining_payment", 0))
        outstanding_debt = float(data.get("outstanding_debt", 0))

        if (remaining_payment - total_amount) >= 0:
            remaining_payment -= total_amount
        else:
            outstanding_debt += (total_amount - remaining_payment)
            remaining_payment = 0.0

        required_amount = outstanding_debt + fixed_fees

        cur.execute("""
            UPDATE farmers
            SET old_counter = ?,
                current_counter = ?,
                consumed = ?,
                total_amount = ?,
                remaining_payment = ?,
                outstanding_debt = ?,
                required_amount = ?,
                last_update = ?
            WHERE id = ?
        """, (
            round(current_counter, 2),
            round(new_counter, 2),
            round(consumed, 2),
            round(total_amount, 2),
            round(remaining_payment, 2),
            round(outstanding_debt, 2),
            round(required_amount, 2),
            datetime.now().strftime("%Y-%m-%d"),
            data["id"]
        ))

        conn.commit()
        conn.close()

        msg = "تم اضافة عداد جديد ? الى ? صاحب رقم البطاقة عدد ? ?"
        Reports.addcounterReport(msg, new_counter, name, cin, counter_number)
        return True

    @staticmethod
    def calcul_total_requird_amount(cin):
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(required_amount), 0) AS total_required_amount
            FROM farmers
            WHERE cin = ?
        """, (str(cin),))
        row = cur.fetchone()
        conn.close()
        return float(row["total_required_amount"] or 0)


def add_all_records():
    records = [
        ("مراد بن محمد سالمي", "07583697", "BS 13", 2243.0, 3389.0, 0.2),
        ("مراد بن محمد سالمي 2", "07583697", "BS 17", 3607.0, 3857.0, 0.2),
        ("نور الدين مجيد سالمي", "01890081", "BS 11", 2646.0, 3473.0, 0.2),
        ("قدور شهيدة سالمي", "07558892", "BS 20", 1454.0, 2155.0, 0.2),
        ("خميس محمد سالم بلغوثي", "02022888", "BS 07", 2327.0, 3197.0, 0.2),
        ("خميس محمد سالم بلغوثي 2", "02022888", "BS 10", 3385.0, 4895.0, 0.2),
        ("خميس محمد سالم بلغوثي 3", "02022888", "BS 08", 3373.0, 4645.0, 0.2),
        ("علي بن مصطفى سالمي", "01949575", "BS 09", 4576.0, 5129.0, 0.2),
        ("لمجد بن محمد سالمي", "07552572", "BS 17", 2811.0, 3507.0, 0.2),
        ("عمر بن احمد سالمي", "01860356", "BS 17", 3507.0, 3607.0, 0.2),
        ("عمر بن احمد سالمي 2", "01860356", "BS 18", 3665.0, 4182.0, 0.2),
        ("منجي محمد علي سالمي", "01965858", "BS 12", 2053.0, 2927.0, 0.2),
        ("حبيب المبروك سالمي", "01887496", "BS 16", 1734.0, 2234.0, 0.2),
        ("محمد المبروك سالمي", "01864121", "BS 16", 2234.0, 2409.0, 0.2),
        ("محمد المبروك سالمي 2", "01864121", "BS 19", 857.0, 1195.0, 0.2),
        ("محمد رضا بلغوثي", "02077242", "BS 06", 4207.0, 5665.0, 0.2),
        ("محمد رضا بلغوثي 2", "02077242", "BS 01", 3938.0, 4177.0, 0.2),
        ("حسونة جملي", "02042359", "BD 06/1", 1516.0, 1951.0, 0.2),
        ("فيصل بلغوثي", "02062330", "BS 01", 2916.0, 3938.0, 0.2),
        ("وناس جملي", "07529930", "BD 03/1", 245.0, 416.0, 0.2),
    ]

    for rec in records:
        Farmers.add(
            name=rec[0],
            cin=rec[1],
            counter_number=rec[2],
            old_counter=rec[3],
            current_counter=rec[4],
            price=rec[5],
            payment=100.0,
            outstanding_debt=0.0,
            fixed_fees=20.0,
        )

    print("تمت إضافة جميع البيانات بنجاح!")