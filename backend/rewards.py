import os
import requests
import pandas as pd
from dotenv import load_dotenv
from helpers import get_top_category_from_db
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def get_active_rewards(username):
    url = f"{SUPABASE_URL}/rest/v1/rewards?username=eq.{username}&used=eq.false&expiry_date=gte.{datetime.today().date()}"
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else []

def add_reward(username, reward_name, category, expiry_date):
    payload = {
        "username": username,
        "reward_name": reward_name,
        "category": category,
        "expiry_date": str(expiry_date)
    }
    url = f"{SUPABASE_URL}/rest/v1/rewards"
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code not in [200, 201]:
        raise Exception(f"Error adding reward: {res.text}")

def suggest_category_coupons(username):
    top_category = get_top_category_from_db(username)
    if not top_category:
        return []

    url = f"{SUPABASE_URL}/rest/v1/rewards?username=eq.{username}&category=eq.{top_category}&used=eq.false&expiry_date=gte.{datetime.today().date()}&limit=2"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        rewards = res.json()
        return [f"🎟️ {r['reward_name']} (expires on {r['expiry_date']})" for r in rewards]
    return []

def auto_generate_reward(username, category, trigger_type="spend"):
    import random
    import string
    from datetime import datetime, timedelta

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

    expiry = (datetime.now() + timedelta(days=30)).date()
    coupon_code = generate_coupon_code(prefix)

    payload = {
        "username": username,
        "reward_name": reward_name,
        "category": category,
        "expiry_date": str(expiry),
        "coupon_code": coupon_code,
        "used": False
    }
    url = f"{SUPABASE_URL}/rest/v1/rewards"
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code not in [200, 201]:
        raise Exception(f"Error adding reward: {res.text}")
    return coupon_code

def generate_coupon_code(prefix="SAVE", length=6):
    import random
    import string
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{suffix}"