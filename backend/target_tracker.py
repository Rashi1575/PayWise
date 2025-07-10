import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def update_target(target_id, new_title, new_amount, new_due_date):
    payload = {
        "title": new_title,
        "target_amount": new_amount,
        "due_date": new_due_date
    }
    url = f"{SUPABASE_URL}/rest/v1/targets?id=eq.{target_id}"
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code not in [200, 204]:
        raise Exception(f"Error updating target: {res.text}")

def delete_target(target_id):
    url = f"{SUPABASE_URL}/rest/v1/targets?id=eq.{target_id}"
    res = requests.delete(url, headers=headers)
    if res.status_code not in [200, 204]:
        raise Exception(f"Error deleting target: {res.text}")

def get_nearing_targets(username, days_threshold=5):
    from datetime import datetime, timedelta
    max_date = (datetime.today() + timedelta(days=days_threshold)).date()
    url = f"{SUPABASE_URL}/rest/v1/targets?username=eq.{username}&due_date=lte.{max_date}"
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else []

def get_monthly_savings(username):
    from datetime import datetime
    now = datetime.now()
    month_prefix = now.strftime("%Y-%m")
    url = f"{SUPABASE_URL}/rest/v1/payments?username=eq.{username}&category=eq.Savings&date=like.{month_prefix}%"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        total = sum((x.get("deposit") or 0) + (x.get("withdrawal") or 0) for x in data)
        return {month_prefix: total}
    return {}

def update_monthly_savings(target_id, new_amount):
    payload = {"savings": new_amount}
    url = f"{SUPABASE_URL}/rest/v1/targets?id=eq.{target_id}"
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code not in [200, 204]:
        raise Exception(f"Error updating savings: {res.text}")

def get_savings_progress(username):
    url = f"{SUPABASE_URL}/rest/v1/savings_targets?username=eq.{username}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200 and res.json():
        row = res.json()[0]
        return row.get("current_savings", 0.0), row.get("target_amount", 0.0)
    return 0.0, 0.0