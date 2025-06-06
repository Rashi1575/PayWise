import hashlib
import psycopg2

# hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="paywise_db",
        user="rashi",
        password="pos@rashi05"
    )
    return conn

def reset_password(username, new_password, confirm_password):
    if new_password != confirm_password:
        print("Passwords do not match!")
        return

    hashed_password = hash_password(new_password)
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
        if cur.fetchone() is None:
            print("Username not found!")
            return

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