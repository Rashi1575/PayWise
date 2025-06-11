from flask import Flask, request, jsonify
from flask_cors import CORS
import signup
import login

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

@app.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([username, email, password, confirm_password]):
        return jsonify({'status': 'fail', 'message': 'All fields are required'}), 400

    try:
        signup.register_user(username, email, password, confirm_password)
        return jsonify({'status': 'success', 'message': 'User registered successfully'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        result = login.authenticate_user(username, password)
        return jsonify({'status': 'success', 'message': 'Login successful' if result else 'Invalid credentials'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
