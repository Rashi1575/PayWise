import os
import random
import psycopg2
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import signup
import login

load_dotenv()  # Load environment variables from .env

# PostgreSQL DB connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 5432))
    )

# Generate a simple math CAPTCHA
def generate_math_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"{a} + {b}", str(a + b)

# Store CAPTCHA in the database
def store_captcha_in_db(question, answer, user_ip=None):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS captcha (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            expires_at TIMESTAMPTZ NOT NULL,
            user_ip TEXT,
            is_used BOOLEAN DEFAULT FALSE
        );
    """)
    cursor.execute("""
        INSERT INTO captcha (question, answer, expires_at, user_ip)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (question, answer, expires_at, user_ip))
    captcha_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return captcha_id

# Validate CAPTCHA
def validate_captcha_from_db(user_input, captcha_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT answer, expires_at, is_used FROM captcha WHERE id = %s;", (captcha_id,))
    result = cursor.fetchone()
    if result:
        correct_answer, expires_at, is_used = result
        if not is_used and datetime.now(timezone.utc) <= expires_at and user_input.strip() == correct_answer.strip():
            cursor.execute("UPDATE captcha SET is_used = TRUE WHERE id = %s;", (captcha_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
    cursor.close()
    conn.close()
    return False

# Handle full CAPTCHA flow
def handle_captcha():
    question, answer = generate_math_captcha()
    captcha_id = store_captcha_in_db(question, answer)
    user_captcha = input(f"\n🤖 CAPTCHA: What is {question}? ").strip()
    if validate_captcha_from_db(user_captcha, captcha_id):
        return True
    else:
        print("❌ CAPTCHA validation failed.")
        return False

# Prompt input from user
def get_user_input(prompt):
    return input(prompt).strip()

# Main Menu
if __name__ == "__main__":
    while True:
        print("\n========= MAIN MENU =========")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        print("=============================")
        choice = get_user_input("Enter your choice: ")

        if choice == '1':  # Register
            username = get_user_input("Enter username: ")
            email = get_user_input("Enter email: ")
            password = get_user_input("Enter password: ")
            confirm_password = get_user_input("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match.")
                continue

            if handle_captcha():
                try:
                    signup.register_user(username, email, password, confirm_password)
                except Exception as e:
                    print(f"Error during registration: {e}")

        elif choice == '2':  # Login
            username = get_user_input("Enter username: ")
            password = get_user_input("Enter password: ")
            if handle_captcha():
                try:
                    login.authenticate_user(username, password)
                except Exception as e:
                    print(f"Error during login: {e}")

        elif choice == '3':  # Password Reset
            username = get_user_input("Enter username: ")
            new_password = get_user_input("Enter new password: ")
            confirm_password = get_user_input("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match.")
                continue

            if handle_captcha():
                try:
                    login.reset_password(username, new_password, confirm_password)
                except Exception as e:
                    print(f"Error during password reset: {e}")

        elif choice == '4':
            print("👋 Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
