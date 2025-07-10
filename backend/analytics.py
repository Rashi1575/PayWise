import os
import requests
import pandas as pd
from dotenv import load_dotenv
from budget import get_monthly_spending, get_top_spending_category, suggest_savings

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}"
}


def load_user_payments(username):
    """
    Fetch user payments from Supabase REST API.
    Returns a DataFrame with all columns + calculated 'amount'.
    """
    url = f"{SUPABASE_URL}/rest/v1/payments?username=eq.{username}"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        data = res.json()
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            # Compute 'amount' as sum of deposit + withdrawal (whichever is present)
            df["amount"] = df[["deposit", "withdrawal"]].sum(axis=1, skipna=True)
        return df
    else:
        raise Exception(f"Error fetching payments: {res.text}")