import pandas as pd
from datetime import datetime, timedelta
from src.utils.db import get_connection
from datetime import date
import random
import string

def get_active_rewards(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT reward_name, category, expiry_date
        FROM rewards
        WHERE user_id = %s AND used = FALSE AND expiry_date >= CURRENT_DATE;
    """
    cursor.execute(query, (user_id,))
    rewards = cursor.fetchall()
    cursor.close()
    conn.close()
    return rewards

def add_reward(user_id, reward_name, category, expiry_date):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO rewards (user_id, reward_name, category, expiry_date)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (user_id, reward_name, category, expiry_date))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_rewards(user_id: str, conn) -> pd.DataFrame:
    """
    Fetch all rewards for a given user from the database.
    Assumes rewards table has: id, user_id, reward_name, category, expiry_date, used (bool)
    """
    query = """
    SELECT reward_name, category, expiry_date, used
    FROM rewards
    WHERE user_id = %s
    """
    df = pd.read_sql(query, conn, params=(user_id,))
    df['expiry_date'] = pd.to_datetime(df['expiry_date'])
    return df


def get_expiring_rewards(df: pd.DataFrame, days_left: int = 7) -> pd.DataFrame:
    """
    Returns rewards expiring in the next `days_left` days.
    """
    today = datetime.today()
    upcoming = today + timedelta(days=days_left)
    expiring = df[(df['expiry_date'] <= upcoming) & (df['used'] == False)]
    return expiring.sort_values(by="expiry_date")


def get_applicable_rewards(df: pd.DataFrame, recent_categories: list) -> list:
    """
    Returns a list of rewards that match recent user spending categories.
    """
    applicable = df[(df['category'].isin(recent_categories)) & (df['used'] == False)]
    return applicable['reward_name'].unique().tolist()

def suggest_category_coupons(user_id):
    """
    Suggest top 2 rewards based on user's highest spending category.
    """
    conn = get_connection()
    
    # Step 1: Find top category
    query = """
        SELECT category, SUM(amount) as total
        FROM payments
        WHERE user_id = %s
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1;
    """
    top_category_result = pd.read_sql(query, conn, params=(user_id,))
    if top_category_result.empty:
        conn.close()
        return []

    top_category = top_category_result.iloc[0]['category']

    # Step 2: Get top 2 unused rewards from that category
    reward_query = """
        SELECT reward_name, expiry_date
        FROM rewards
        WHERE user_id = %s AND category = %s AND used = FALSE AND expiry_date >= CURRENT_DATE
        ORDER BY expiry_date ASC
        LIMIT 2;
    """
    rewards_df = pd.read_sql(reward_query, conn, params=(user_id, top_category))
    conn.close()

    # Step 3: Format response
    result = []
    for _, row in rewards_df.iterrows():
        result.append(f"🎟️ {row['reward_name']} (expires on {row['expiry_date'].date()})")
    return result

def auto_generate_reward(user_id, category, trigger_type="spend"):
    """
    Creates a reward entry with a random coupon code.
    """
    from datetime import datetime, timedelta

    # Define message
    if trigger_type == "spend":
        reward_name = f"🎁 10% Cashback on next {category}"
        prefix = "SAVE10"
    elif trigger_type == "savings":
        reward_name = "🎯 ₹50 Bonus for hitting your savings goal!"
        prefix = "BONUS50"
    elif trigger_type == "loyalty":
        reward_name = "💎 Loyalty Reward: ₹100 off"
        prefix = "LOYALTY"
    else:
        reward_name = "🎉 Thank you reward"
        prefix = "THANKS"

    expiry = datetime.now() + timedelta(days=30)
    coupon_code = generate_coupon_code(prefix)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rewards (user_id, reward_name, category, expiry_date, coupon_code, used)
        VALUES (%s, %s, %s, %s, %s, FALSE)
    """, (user_id, reward_name, category, expiry, coupon_code))
    conn.commit()
    cur.close()
    conn.close()

    return coupon_code


def format_expiring_rewards(expiring_df: pd.DataFrame) -> list:
    """
    Return user-friendly strings for rewards expiring soon.
    """
    formatted = []
    for _, row in expiring_df.iterrows():
        remaining = (row['expiry_date'] - datetime.today()).days
        formatted.append(f"'{row['reward_name']}' in '{row['category']}' expires in {remaining} day(s).")
    return formatted

def generate_coupon_code(prefix="SAVE", length=6):
    """Generate a unique coupon code like SAVE-XD93K2"""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{suffix}"
