import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = DATABASE_DIR / "expenses.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    connection = sqlite3.connect(
        str(DB_PATH)
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT NOT NULL,

            type TEXT NOT NULL,

            category TEXT NOT NULL,

            amount REAL NOT NULL,

            payment TEXT DEFAULT '',

            description TEXT DEFAULT '',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# ADD TRANSACTION
# ============================================================

def add_transaction(
    transaction_date,
    transaction_type,
    category,
    amount,
    payment="",
    description=""
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (
            date,
            type,
            category,
            amount,
            payment,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transaction_date,
        transaction_type,
        category,
        float(amount),
        payment,
        description
    ))

    connection.commit()

    transaction_id = cursor.lastrowid

    connection.close()

    return transaction_id


# ============================================================
# UPDATE TRANSACTION
# ============================================================

def update_transaction(
    transaction_id,
    transaction_date,
    transaction_type,
    category,
    amount,
    payment="",
    description=""
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions

        SET
            date = ?,
            type = ?,
            category = ?,
            amount = ?,
            payment = ?,
            description = ?

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

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


# ============================================================
# DELETE TRANSACTION
# ============================================================

def delete_transaction(transaction_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (
        transaction_id,
    ))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


# ============================================================
# GET SINGLE TRANSACTION
# ============================================================

def get_transaction(transaction_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE id = ?
    """, (
        transaction_id,
    ))

    transaction = cursor.fetchone()

    connection.close()

    return transaction


# ============================================================
# GET ALL TRANSACTIONS
# ============================================================

def get_all_transactions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# GET TRANSACTIONS BY TYPE
# ============================================================

def get_transactions_by_type(transaction_type):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE type = ?
        ORDER BY date DESC, id DESC
    """, (
        transaction_type,
    ))

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# TOTAL INCOME
# ============================================================

def get_total_income():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(
            SUM(amount),
            0
        )

        FROM transactions

        WHERE type = 'Income'
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return float(total)


# ============================================================
# TOTAL EXPENSE
# ============================================================

def get_total_expense():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(
            SUM(amount),
            0
        )

        FROM transactions

        WHERE type = 'Expense'
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return float(total)


# ============================================================
# BALANCE
# ============================================================

def get_balance():

    return (
        get_total_income()
        - get_total_expense()
    )


# ============================================================
# CURRENT MONTH EXPENSE
# ============================================================

def get_current_month_expense():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(
            SUM(amount),
            0
        )

        FROM transactions

        WHERE type = 'Expense'

        AND strftime(
            '%Y-%m',
            date
        ) = strftime(
            '%Y-%m',
            'now'
        )
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return float(total)


# ============================================================
# EXPENSES BY CATEGORY
# ============================================================

def get_expenses_by_category():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total

        FROM transactions

        WHERE type = 'Expense'

        GROUP BY category

        ORDER BY total DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# MONTHLY SUMMARY
# ============================================================

def get_monthly_summary():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            strftime(
                '%Y-%m',
                date
            ) AS month,

            SUM(
                CASE
                    WHEN type = 'Income'
                    THEN amount
                    ELSE 0
                END
            ) AS income,

            SUM(
                CASE
                    WHEN type = 'Expense'
                    THEN amount
                    ELSE 0
                END
            ) AS expense

        FROM transactions

        GROUP BY month

        ORDER BY month ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# RECENT TRANSACTIONS
# ============================================================

def get_recent_transactions(limit=10):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY date DESC, id DESC
        LIMIT ?
    """, (
        limit,
    ))

    rows = cursor.fetchall()

    connection.close()

    return rows