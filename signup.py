import hashlib
import psycopg2
from otp import send_otp, verify_otp  # Make sure this file exists with those functions

# Hash password securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Get DB connection
def get_db_connection():
    return psycopg2.connect(
        host="db.havcrxnjjopcwjhtiytp.supabase.co",
        database="postgres",
        user="postgres",
        password="AdiKpish@00",  # Use .env for real deployment
        port=5432
    )

# Create users table (with email)
def create_users_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Check if username exists
def username_exists(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists

# Final registration flow
def register_user(username, email, password, confirm_password):
    if not email.strip():
        print("Email cannot be empty!")
        return

    if password != confirm_password:
        print("Passwords do not match!")
        return

    if username_exists(username):
        print("Username already exists!")
        return

    # Send OTP
    sent, msg = send_otp(email)
    print(msg)
    if not sent:
        return

    # Verify OTP
    otp_input = input("Enter the OTP sent to your email: ").strip()
    verified, verify_msg = verify_otp(email, otp_input)
    print(verify_msg)
    if not verified:
        return

    # Hash password and insert
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);",
            (username, email, hashed_password)
        )
        conn.commit()
        print("User registered successfully!")
    except Exception as e:
        print(f"❌ Error registering user: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Ensure table exists on first run
if __name__ == "__main__":
    create_users_table()  # <- run once
