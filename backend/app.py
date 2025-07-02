from flask import Flask, request, jsonify
from flask_cors import CORS
from login import authenticate_user, reset_password
from signup import register_user
from otp import send_otp, verify_otp
import os
import requests

app = Flask(__name__)
CORS(app)  # Allow frontend to connect
# CORS(app, origins=["http://localhost:3000"])

# Supabase RESTful config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
TABLE = os.getenv("SUPABASE_USERS_TABLE", "users")

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
    otp = data['otp']  # important

    try:
        # login.reset_password(username, new_password, confirm_password, otp)
        reset_password(username, new_password, confirm_password, otp)
        return jsonify({"success": True, "message": "Password reset!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
# NEWW
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
