
import os
import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
TABLE = os.getenv("SUPABASE_USERS_TABLE", "users")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}"
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    hashed_password = hash_password(password)

    # ✅ Only filter by username — fetch the user
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}&select=password"
    res = requests.get(url, headers=headers)

    if res.status_code == 200 and res.json():
        db_password = res.json()[0]['password']
        print("🔒 Supabase stored hash:", db_password)
        print("🔐 Hash of entered password:", hashed_password)

        if hashed_password == db_password:
            return True
        else:
            print("❌ Password mismatch.")
    else:
        print("❌ User not found or Supabase error.")

    return False
    
# ✅ Reset password using OTP (email must already be verified)
def reset_password(username, new_password, confirm_password, otp):
    if new_password != confirm_password:
        raise Exception("Passwords do not match!")

    # Step 1: Get user email from username
    user_url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}&select=email"
    user_res = requests.get(user_url, headers=headers)

    if user_res.status_code != 200 or not user_res.json():
        raise Exception("Username not found!")

    email = user_res.json()[0]['email']

    # Step 2: ✅ Do NOT re-verify OTP (already verified before calling this)

    # Step 3: Update password
    hashed = hash_password(new_password)
    update_url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}"
    update_res = requests.patch(update_url, headers=headers | {"Content-Type": "application/json"}, json={"password": hashed})

    if update_res.status_code in [200, 204]:
        print("✅ Password reset successful.")
    else:
        raise Exception(f"❌ Password reset failed: {update_res.text}")


