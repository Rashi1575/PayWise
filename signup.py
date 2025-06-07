import hashlib
import psycopg2
from psycopg2 import sql

# hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="db.havcrxnjjopcwjhtiytp.supabase.co",
        database="postgres",
        user="postgres",
        password="AdiKpish@00",  # Consider using environment variables!
        port=5432
    )
    return conn

# Create users table if it does not exist
def create_users_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
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

# Register user into PostgreSQL
def register_user(username, password, confirm_password):
    if password != confirm_password:
        print("Passwords do not match!")
        return

    if username_exists(username):
        print("Username already exists!")
        return

    hashed_password = hash_password(password)

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);",
            (username, hashed_password)
        )
        conn.commit()
        print("User registered successfully!")
    except Exception as e:
        print(f"Error registering user: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

