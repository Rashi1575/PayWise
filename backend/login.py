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
        return cur.fetchone() is not None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return False
    finally:
        cur.close()
        conn.close()


#Reset password using OTP verification
# def reset_password(username, new_password, confirm_password, otp):
#     if new_password != confirm_password:
#         raise Exception("Passwords do not match!")

#     conn = get_db_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute("SELECT email FROM users WHERE username = %s;", (username,))
#         result = cur.fetchone()
#         if result is None:
#             raise Exception("Username not found!")

#         email = result[0]
#         # verified, verify_msg = verify_otp(email, otp)
#         # if not verified:
#         #     raise Exception("OTP verification failed: " + verify_msg)

#         hashed_password = hash_password(new_password)
#         cur.execute(
#             "UPDATE users SET password = %s WHERE username = %s;",
#             (hashed_password, username)
#         )
#         conn.commit()

#     except Exception as e:
#         conn.rollback()
#         raise Exception(f"Error resetting password: {e}")
#     finally:
#         cur.close()
#         conn.close()

def reset_password(username, new_password, confirm_password, otp):
    if new_password != confirm_password:
        raise Exception("Passwords do not match!")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT email FROM users WHERE username = %s;", (username,))
        result = cur.fetchone()
        if result is None:
            raise Exception("Username not found!")

        email = result[0]

        # ❌ DO NOT verify OTP again here

        hashed_password = hash_password(new_password)
        cur.execute(
            "UPDATE users SET password = %s WHERE username = %s;",
            (hashed_password, username)
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise Exception(f"Error resetting password: {e}")
    finally:
        cur.close()
        conn.close()




