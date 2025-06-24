# Existing imports
import psycopg2
from datetime import datetime, timedelta
from src.utils.db import get_connection

# Connect DB (reuse)
def get_connection():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

# UPDATE target
def update_target(target_id, new_title, new_amount, new_due_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE targets
        SET title = %s, target_amount = %s, due_date = %s
        WHERE id = %s
    """, (new_title, new_amount, new_due_date, target_id))
    conn.commit()
    cursor.close()
    conn.close()

# DELETE target
def delete_target(target_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM targets WHERE id = %s", (target_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Check nearing deadline (returns list of urgent targets)
def get_nearing_targets(user_id, days_threshold=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, due_date FROM targets
        WHERE user_id = %s AND due_date <= CURRENT_DATE + INTERVAL '%s day'
    """, (user_id, days_threshold))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Monthly savings graph data (returns {month: total_savings})
def get_monthly_savings(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_TRUNC('month', date) as month, SUM(amount)
        FROM payments
        WHERE user_id = %s AND category = 'Savings'
        GROUP BY month
        ORDER BY month
    """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return {str(r[0].date()): r[1] for r in results}

def update_monthly_savings(target_id, new_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE targets
        SET savings=%s
        WHERE id = %s
    """, (new_amount, target_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_savings_progress(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT target_amount, current_savings FROM savings_targets
            WHERE user_id = %s
        """, (user_id,))
        row = cur.fetchone()
    conn.close()

    if row:
        return row[1], row[0]  # (savings, goal)
    return 0.0, 0.0