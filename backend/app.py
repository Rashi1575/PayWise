from flask import Flask, request, jsonify
from flask_cors import CORS
from login import authenticate_user, reset_password
from signup import register_user
from otp import send_otp, verify_otp
import os
import joblib
import datetime
import supabase
from supabase import create_client
import pandas as pd
import requests
from supabase import create_client, Client
from datetime import datetime
import uuid
from rewards import get_active_rewards
from rewards import add_reward
from rewards import suggest_category_coupons
from rewards import auto_generate_reward

from dotenv import load_dotenv
load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
TABLE = os.getenv("SUPABASE_USERS_TABLE", "users")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY) #Rashi

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# CORS(app)   Allow frontend to connect

def generate_transaction_id(username, prefix="TXN"):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # till ms
    return f"{prefix}{timestamp}_{username.upper()[0]}"

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    print("📬 /signup API hit")
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']
    
    try:
        register_user(username, email, password, confirm_password)
        return jsonify({"success": True, "message": "User registered! Check email for OTP."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        if authenticate_user(username, password):
            return jsonify({"success": True, "message": "Login successful!"})
        else:
            return jsonify({"success": False, "error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401

# Forgot Password Route
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    username = data['username']
    new_password = data['new_password']
    confirm_password = data['confirm_password']
    otp = data['otp']  # ✅ important

    try:
        reset_password(username, new_password, confirm_password, otp)
        return jsonify({"success": True, "message": "Password reset!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/get-email', methods=['POST'])
def get_email_by_username():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({"success": False, "message": "Username missing"}), 400

    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}&select=email"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200 and res.json():
        email = res.json()[0]['email']
        return jsonify({"success": True, "email": email})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

# OTP Routes
@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    email = request.get_json()['email']
    success, message = send_otp(email)
    return jsonify({"success": success, "message": message})

@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    email = data['email']
    otp = data['otp']
    success, message = verify_otp(email, otp)
    return jsonify({"success": success, "message": message})

#NEW
@app.route('/profile/<username>', methods=['GET'])
def get_profile(username):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}&select=full_name,email,phone,gender,nationality,address"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.json():
        return jsonify({"success": True, "data": response.json()[0]})
    else:
        return jsonify({"success": False, "error": "User not found"}), 404

@app.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({"success": False, "error": "Username is required"}), 400

    # Prepare update fields dynamically
    update_fields = {
        "full_name": data.get("full_name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "gender": data.get("gender"),
        "nationality": data.get("nationality"),
        "address": data.get("address"),
    }

    # Remove None fields (only send updates for provided fields)
    update_fields = {k: v for k, v in update_fields.items() if v is not None}

    if not update_fields:
        return jsonify({"success": False, "error": "No fields to update"}), 400

    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?username=eq.{username}"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    response = requests.patch(url, headers=headers, json=update_fields)

    if response.status_code in (200, 204):
        return jsonify({"success": True, "message": "Profile updated"})
    else:
        return jsonify({"success": False, "error": response.text}), 400

# Load ML models
expense_clf = joblib.load("expense_classifier_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")  # If you saved it separately
fraud_model = joblib.load("fraud_model.pkl")

# Rashi
@app.route('/budgets', methods=['GET', 'POST', 'OPTIONS'])
def budgets():
    if request.method == 'OPTIONS':
        return '', 200

    if request.method == 'GET':
        username = request.args.get('username')
        try:
            response = supabase.table("budgets").select("*").eq("username", username).execute()
            data = response.data
            return jsonify({"success": True, "data": data})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    if request.method == 'POST':
        try:
            body = request.get_json()
            username = body.get("username")
            category = body.get("category")
            budget_amount = body.get("budget_amount")

            if not username or not category or budget_amount is None:
                print("❌ Missing fields:", body)
                return jsonify({
                    "success": False,
                    "error": "Missing required fields: username, category, or budget_amount"
                }), 400

            # Check if entry exists
            existing = supabase.table("budgets").select("id").eq("username", username).eq("category", category).execute()

            if existing.data:
                # Update
                budget_id = existing.data[0]['id']
                response = supabase.table("budgets").update({
                    "budget_amount": budget_amount
                }).eq("id", budget_id).execute()
            else:
                # Insert
                response = supabase.table("budgets").insert({
                    "username": username,
                    "category": category,
                    "budget_amount": budget_amount
                }).execute()

            return jsonify({"success": True, "data": response.data})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
# Rashi
@app.route("/make-payment", methods=["POST"])
def make_payment():
    try:
        data = request.get_json(force=True)
        sender = data.get("sender", "").strip()
        receiver = data.get("receiver", "").strip()
        amount = float(data.get("amount", 0))
        description = data.get("description", "").strip() or "No description"
        method = data.get("method", "").strip() or "Other"
        date_today = datetime.now().strftime("%Y-%m-%d")

        # Safety check
        if not all([sender, receiver]) or amount <= 0:
            return jsonify({"success": False, "message": "Missing or invalid fields."}), 400

        # Fetch sender's balance
        sender_data = supabase.table("payments").select("closing_balance").eq("username", sender).order("date", desc=True).limit(1).execute()
        sender_balance = sender_data.data[0]["closing_balance"] if sender_data.data else 10000.0

        if amount > sender_balance:
            return jsonify({"success": False, "message": "Insufficient balance."}), 400

        # Deduct from sender
        new_sender_balance = sender_balance - amount
        txn_id_sender = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S%f") + "_S"

        supabase.table("payments").insert({
            "transaction_id": txn_id_sender,
            "username": sender,
            "category": "Transfer",
            "description": description,
            "payment_method": method,
            "is_fraud": False,
            "deposit": None,
            "withdrawal": amount,
            "closing_balance": new_sender_balance,
            "date": date_today
        }).execute()

        # Fetch receiver's balance
        receiver_data = supabase.table("payments").select("closing_balance").eq("username", receiver).order("date", desc=True).limit(1).execute()
        receiver_balance = receiver_data.data[0]["closing_balance"] if receiver_data.data else 10000.0
        new_receiver_balance = receiver_balance + amount
        txn_id_receiver = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S%f") + "_R"

        # Credit to receiver
        supabase.table("payments").insert({
            "transaction_id": txn_id_receiver,
            "username": receiver,
            "category": "Transfer",
            "description": f"Received from {sender}: {description}",
            "payment_method": method,
            "is_fraud": False,
            "deposit": amount,
            "withdrawal": None,
            "closing_balance": new_receiver_balance,
            "date": date_today
        }).execute()

        return jsonify({"success": True, "message": "Payment successful."})

    except Exception as e:
        print("❌ Payment Error:", str(e))
        return jsonify({"success": False, "message": "Payment failed. Please try again."}), 500

    
# Rashi
@app.route('/targets', methods=['GET', 'POST', 'OPTIONS'])
def targets():
    if request.method == 'OPTIONS':
        return '', 200

    if request.method == 'GET':
        username = request.args.get('username')
        try:
            response = supabase.table("targets").select("*").eq("username", username).execute()
            return jsonify({"success": True, "data": response.data})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    if request.method == 'POST':
        data = request.get_json()
        username     = data["username"]
        title        = data["title"]
        target_amt   = data["target_amount"]
        due_date     = data["due_date"]
        savings_amt  = data.get("savings", 0)

        # 1) Upsert into the `targets` table (you already have this)
        existing = supabase.table("targets")\
            .select("id")\
            .eq("username", username)\
            .eq("title", title)\
            .execute()

        if existing.data:
            target_id = existing.data[0]["id"]
            supabase.table("targets").update({
                "target_amount": target_amt,
                "due_date": due_date,
                "savings": savings_amt
            }).eq("id", target_id).execute()
        else:
            supabase.table("targets").insert({
                "username": username,
                "title": title,
                "target_amount": target_amt,
                "due_date": due_date,
                "savings": savings_amt
            }).execute()

        # 2) Now upsert into `savings_targets` so current_savings is kept in that table too
        #    (this table has username as primary key)
        existing_st = supabase.table("savings_targets")\
            .select("username")\
            .eq("username", username)\
            .execute()

        if existing_st.data:
            supabase.table("savings_targets").update({
                "current_savings": savings_amt,
                "target_amount": target_amt
            }).eq("username", username).execute()
        else:
            supabase.table("savings_targets").insert({
                "username": username,
                "current_savings": savings_amt,
                "target_amount": target_amt
            }).execute()

        return jsonify({"success": True})



@app.route("/get-payments", methods=["POST"])
def get_payments():
    data = request.get_json()
    username = data["username"]

    result = supabase.table("payments").select("*").eq("username", username).order("date", desc=True).execute()

    return jsonify({"success": True, "payments": result.data})

@app.route("/spending-insights", methods=["POST"])
def spending_insights():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"success": False, "error": "Username required"}), 400

    try:
        # Fetch user's payments (excluding fraud)
        result = supabase.table("payments") \
            .select("category, withdrawal") \
            .eq("username", username) \
            .eq("is_fraud", False) \
            .execute()

        payments = result.data
        category_totals = {}
        total_spent = 0

        for txn in payments:
            cat = txn["category"]
            amt = txn["withdrawal"] or 0
            category_totals[cat] = category_totals.get(cat, 0) + amt
            total_spent += amt

        # Determine highest category
        highest_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else "N/A"

        # Return data
        return jsonify({
            "success": True,
            "total_spent": total_spent,
            "category_totals": category_totals,
            "highest_category": highest_category
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/get-rewards", methods=["POST"])
def get_rewards():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"success": False, "error": "Username required"}), 400

    try:
        rewards = get_active_rewards(username)
        return jsonify({"success": True, "rewards": rewards})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add-reward", methods=["POST"])
def add_reward_route():
    data = request.get_json()
    username = data.get("username")
    reward_name = data.get("reward_name")
    category = data.get("category")
    expiry_date = data.get("expiry_date")

    if not all([username, reward_name, category, expiry_date]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    try:
        add_reward(username, reward_name, category, expiry_date)
        return jsonify({"success": True, "message": "Reward added!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/suggest-rewards", methods=["POST"])
def suggest_rewards():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"success": False, "error": "Username required"}), 400

    try:
        suggestions = suggest_category_coupons(username)
        return jsonify({"success": True, "suggestions": suggestions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/auto-generate-reward", methods=["POST"])
def auto_generate_reward_route():
    data = request.get_json()
    username = data.get("username")
    category = data.get("category")
    trigger_type = data.get("trigger_type", "spend")

    if not username or not category:
        return jsonify({"success": False, "error": "Missing username or category"}), 400

    try:
        coupon = auto_generate_reward(username, category, trigger_type)
        return jsonify({"success": True, "coupon_code": coupon})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)
