import pandas as pd
import datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.email_service import send_email
from src.utils.db import get_connection
from src.utils.db import get_user_email  # Updated import
from datetime import datetime
from src.dashboard.rewards import get_active_rewards, add_reward

def set_budget(user_id, category, amount):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO budgets (user_id, category, budget_amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, category)
            DO UPDATE SET budget_amount = EXCLUDED.budget_amount, updated_at = NOW()
        """, (user_id, category, amount))
        conn.commit()
    conn.close()

def get_budget(user_id, category=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT budget_amount, spent_amount FROM budgets
            WHERE user_id = %s AND category IS NOT DISTINCT FROM %s
        """, (user_id, category))
        row = cur.fetchone()
    conn.close()
    return row if row else (0.0, 0.0)


def get_total_monthly_spending(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT SUM(amount)
        FROM payments
        WHERE user_id = %s
          AND date_trunc('month', date) = date_trunc('month', CURRENT_DATE);
    """
    cursor.execute(query, (user_id,))
    total = cursor.fetchone()[0] or 0.0
    cursor.close()
    conn.close()
    return round(total, 2)


def get_current_month_year():
    today = datetime.date.today()
    return today.month, today.year

def get_monthly_spending(df: pd.DataFrame) -> float:
    """Returns total spending for the current month."""
    month, year = get_current_month_year()
    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]
    return monthly_df['amount'].sum()

def get_top_spending_category(df: pd.DataFrame) -> str:
    """Returns the highest spending category for the current month."""
    month, year = get_current_month_year()
    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]
    if monthly_df.empty:
        return "No Data"
    top_category = monthly_df.groupby('category')['amount'].sum().idxmax()
    return top_category

def suggest_savings(df: pd.DataFrame) -> list:
    """
    Rule-based ML suggestion: Identify top 3 spending categories this month,
    and recommend saving % for each.
    """
    suggestions = []
    month, year = get_current_month_year()
    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]

    if monthly_df.empty:
        return ["Not enough data for suggestions."]
    
    category_spending = monthly_df.groupby('category')['amount'].sum().sort_values(ascending=False)
    top_categories = category_spending.head(3)

    for category, amount in top_categories.items():
        suggestion = f"Try reducing expenses in '{category}' by 10% (~₹{round(amount * 0.1, 2)})."
        suggestions.append(suggestion)

    return suggestions
