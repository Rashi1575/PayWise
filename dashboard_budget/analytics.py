import psycopg2
import pandas as pd
from datetime import datetime
import src.dashboard.budget as budget

def get_monthly_spending(df):
    return round(budget.get_monthly_spending(df), 2)

def get_top_spending_category(df):
    return budget.get_top_spending_category(df)

def suggest_savings(df):
    return budget.suggest_savings(df)

def connect_db():
    return psycopg2.connect(
        host="localhostdb.havcrxnjjopcwjhtiytp.supabase.co",         # or your DB host
        database="postgres",  # replace with your DB name
        user="postgres",     # your DB username
        password="AdiKpish@00"  # your DB password
    )
#USER PAYMENTS
def load_user_payments(user_id):
    conn = connect_db()
    query = """
        SELECT amount, category, date 
        FROM payments 
        WHERE user_id = %s
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    df['date'] = pd.to_datetime(df['date'])
    conn.close()
    return df

def get_monthly_spending(df):
    current_month = datetime.now().strftime('%Y-%m')
    this_month_df = df[df['date'].dt.strftime('%Y-%m') == current_month]
    return round(this_month_df['amount'].sum(), 2)

def get_top_spending_category(df):
    current_month = datetime.now().strftime('%Y-%m')
    this_month_df = df[df['date'].dt.strftime('%Y-%m') == current_month]
    if this_month_df.empty:
        return "No data"
    return this_month_df.groupby('category')['amount'].sum().idxmax()

def suggest_savings(df):
    current_month = datetime.now().strftime('%Y-%m')
    df = df[df['date'].dt.strftime('%Y-%m') == current_month]
    if df.empty:
        return ["No spending data available to suggest savings."]
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    suggestions = []
    for category, amount in category_totals.head(3).items():
        suggestions.append(f"Consider reducing expenses in '{category}' (₹{amount:.2f})")
    return suggestions



