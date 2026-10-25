import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "expenses.db"


# ============================================================
# HELPERS
# ============================================================

def get_connection():
    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def _run(sql, params=(), fetch=None):
    """
    Run one SQL statement and close the connection.

    fetch=None  -> write query; returns the cursor (rowcount / lastrowid)
    fetch="one" -> returns a single row
    fetch="all" -> returns all rows
    """
    connection = get_connection()
    try:
        cursor = connection.execute(sql, params)

        if fetch == "one":
            return cursor.fetchone()
        if fetch == "all":
            return cursor.fetchall()

        connection.commit()
        return cursor.rowcount, cursor.lastrowid
    finally:
        connection.close()


def _total(sql, params=()):
    """Run a single-value query (e.g. SUM) and return it as a float."""
    return float(_run(sql, params, fetch="one")[0])


# ============================================================
# SETUP
# ============================================================

def initialize_database():
    _run("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            payment TEXT DEFAULT '',
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


# ============================================================
# ADD / UPDATE / DELETE
# ============================================================

def add_transaction(
    transaction_date,
    transaction_type,
    category,
    amount,
    payment="",
    description=""
):
    _, transaction_id = _run("""
        INSERT INTO transactions
            (date, type, category, amount, payment, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transaction_date,
        transaction_type,
        category,
        float(amount),
        payment,
        description
    ))
    return transaction_id


def update_transaction(
    transaction_id,
    transaction_date,
    transaction_type,
    category,
    amount,
    payment="",
    description=""
):
    rows_changed, _ = _run("""
        UPDATE transactions
        SET date = ?, type = ?, category = ?,
            amount = ?, payment = ?, description = ?
        WHERE id = ?
    """, (
        transaction_date,
        transaction_type,
        category,
        float(amount),
        payment,
        description,
        transaction_id
    ))
    return rows_changed > 0


def delete_transaction(transaction_id):
    rows_changed, _ = _run(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )
    return rows_changed > 0


# ============================================================
# READ TRANSACTIONS
# ============================================================

def get_transaction(transaction_id):
    return _run(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,),
        fetch="one"
    )


def get_all_transactions():
    return _run(
        "SELECT * FROM transactions ORDER BY date DESC, id DESC",
        fetch="all"
    )


def get_transactions_by_type(transaction_type):
    return _run(
        """
        SELECT * FROM transactions
        WHERE type = ?
        ORDER BY date DESC, id DESC
        """,
        (transaction_type,),
        fetch="all"
    )


def get_recent_transactions(limit=10):
    return _run(
        """
        SELECT * FROM transactions
        ORDER BY date DESC, id DESC
        LIMIT ?
        """,
        (limit,),
        fetch="all"
    )


# ============================================================
# TOTALS
# ============================================================

def get_total_income():
    return _total("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'Income'
    """)


def get_total_expense():
    return _total("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'Expense'
    """)


def get_balance():
    return get_total_income() - get_total_expense()


def get_current_month_expense():
    return _total("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'Expense'
          AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)


# ============================================================
# REPORTS
# ============================================================

def get_expenses_by_category():
    return _run("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
    """, fetch="all")


def get_monthly_summary():
    return _run("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(CASE WHEN type = 'Income'  THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS expense
        FROM transactions
        GROUP BY month
        ORDER BY month ASC
    """, fetch="all")
