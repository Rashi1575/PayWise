import hashlib
import psycopg2
from otp import send_otp, verify_otp  # Make sure your otp.py is configured properly

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Establish database connection
def get_db_connection():
    return psycopg2.connect(
        host="db.havcrxnjjopcwjhtiytp.supabase.co",
        database="postgres",
        user="postgres",
        password="AdiKpish@00",  # 🔐 Use environment variables in production
        port=5432
    )

# Authenticate user login
def authenticate_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT 1 FROM users WHERE username = %s AND password = %s;",
            (username, hashed_password)
        )
        if cur.fetchone():
            print("Login successful!")
        else:
            print("Invalid username or password.")
    except Exception as e:
        print(f"Error during authentication: {e}")
    finally:
        cur.close()
        conn.close()

# Reset password using OTP verification
def reset_password(username, new_password, confirm_password):
    if new_password != confirm_password:
        print("Passwords do not match!")
        return

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Step 1: Check if user exists & get their email
        cur.execute("SELECT email FROM users WHERE username = %s;", (username,))
        result = cur.fetchone()
        if result is None:
            print("Username not found!")
            return
        email = result[0]

        # Step 2: Send OTP to registered email
        sent, msg = send_otp(email)
        print(msg)
        if not sent:
            return

        # Step 3: Verify OTP
        otp_input = input("Enter the OTP sent to your email: ").strip()
        verified, verify_msg = verify_otp(email, otp_input)
        print(verify_msg)
        if not verified:
            return

        # Step 4: Update password
        hashed_password = hash_password(new_password)
        cur.execute(
            "UPDATE users SET password = %s WHERE username = %s;",
            (hashed_password, username)
        )
        conn.commit()
        print("Password reset successfully!")

    except Exception as e:
        print(f"Error resetting password: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

