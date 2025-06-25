from flask import Flask, request, jsonify
from flask_cors import CORS
from login import authenticate_user, reset_password
from signup import register_user
from otp import send_otp, verify_otp
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

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
        login.reset_password(username, new_password, confirm_password, otp)
        return jsonify({"success": True, "message": "Password reset!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400




# OTP Routes
@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    email = request.get_json()['email']
    success, message = send_otp(email)
    return jsonify({"success": success, "message": message})

# @app.route('/verify-otp', methods=['POST'])
# def verify_otp_route():
#     email = request.get_json()['email']
#     otp = request.get_json()['otp']
#     success, message = verify_otp(email, otp)
#     return jsonify({"success": success, "message": message})
@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    email = data['email']
    otp = data['otp']
    success, message = verify_otp(email, otp)
    return jsonify({"success": success, "message": message})



if __name__ == '__main__':
    app.run(debug=True, port=5000)