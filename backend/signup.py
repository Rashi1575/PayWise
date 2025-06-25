

import os
import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()

# ✅ Supabase RESTful config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
TABLE = os.getenv("SUPABASE_USERS_TABLE", "users")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

# ✅ Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Check if username exists in Supabase
def username_exists(username):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}"
    res = requests.get(url, headers=headers)
    return res.status_code == 200 and bool(res.json())

# ✅ Final registration function (logic unchanged, just via Supabase REST)
def register_user(username, email, password, confirm_password):
    print("📨 Signup called with:")
    print(f"Username: {username}, Email: {email}")

    if not email.strip():
        raise Exception("Email cannot be empty.")

    if password != confirm_password:
        raise Exception("Passwords do not match.")

    if username_exists(username):
        raise Exception("Username already exists.")

    hashed_password = hash_password(password)

    # ✅ Insert user via REST API
    payload = {
        "username": username,
        "email": email,
        "password": hashed_password
    }

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/{TABLE}",
        headers=headers,
        json=payload
    )

    if res.status_code == 201:
        print("✅ User registered successfully.")
    else:
        print("❌ Error inserting user:", res.text)
        raise Exception("Signup failed.")

