import os
import requests
import pandas as pd
from dotenv import load_dotenv
from rewards import get_active_rewards, add_reward
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def set_budget(username, category, amount):
    payload = {
        "username": username,
        "category": category,
        "budget_amount": amount
    }
    url = f"{SUPABASE_URL}/rest/v1/budgets"
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code not in [200, 201]:
        raise Exception(f"Error setting budget: {res.text}")

def get_budget(username, category=None):
    query = f"username=eq.{username}"
    if category:
        query += f"&category=eq.{category}"
    url = f"{SUPABASE_URL}/rest/v1/budgets?{query}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200 and res.json():
        row = res.json()[0]
        return row["budget_amount"], row.get("spent_amount", 0.0)
    return (0.0, 0.0)

def get_total_monthly_spending(username):
    from datetime import datetime
    now = datetime.now()
    month = now.strftime("%Y-%m")
    url = f"{SUPABASE_URL}/rest/v1/payments?username=eq.{username}&date=like.{month}%"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        total = sum((x.get("deposit") or 0) + (x.get("withdrawal") or 0) for x in data)
        return round(total, 2)
    return 0.0

def get_current_month_year():
    today = datetime.date.today()
    return today.month, today.year

def get_monthly_spending(df: pd.DataFrame) -> float:
    month, year = get_current_month_year()
    if df.empty:
        return 0.0
    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]
    return monthly_df['amount'].sum()

def get_top_spending_category(df: pd.DataFrame) -> str:
    month, year = get_current_month_year()
    if df.empty:
        return "No Data"
    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]
    if monthly_df.empty:
        return "No Data"
    return monthly_df.groupby('category')['amount'].sum().idxmax()

def suggest_savings(df: pd.DataFrame) -> list:
    month, year = get_current_month_year()
    if df.empty:
        return ["Not enough data."]
    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]
    if monthly_df.empty:
        return ["Not enough data."]
    category_spending = monthly_df.groupby('category')['amount'].sum().sort_values(ascending=False)
    suggestions = []
    for category, amount in category_spending.head(3).items():
        suggestions.append(f"Try reducing expenses in '{category}' by 10% (~₹{round(amount * 0.1, 2)}).")
    return suggestions

def get_top_category_from_db(username):
    url = f"{SUPABASE_URL}/rest/v1/payments?username=eq.{username}&select=category,deposit,withdrawal"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if df.empty:
            return None
        df["amount"] = df[["deposit", "withdrawal"]].sum(axis=1, skipna=True)
        top_category = df.groupby("category")["amount"].sum().idxmax()
        return top_category
    return None
