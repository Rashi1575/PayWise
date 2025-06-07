import signup
import login
import psycopg2
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT",5432)
    )

# Example usage in your code:
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users;")
print(cursor.fetchall())

def get_user_input(prompt):
    return input(prompt).strip()

if __name__ == "__main__":
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = get_user_input("Enter your choice: ")

        if choice == '1':
            username = get_user_input("Enter username: ")
            password = get_user_input("Enter password: ")             # no getpass here
            confirm_password = get_user_input("Confirm password: ")   # no getpass here
            try:
                signup.register_user(username, password, confirm_password)
            except Exception as e:
                print(f"Error during registration: {e}")

        elif choice == '2':
            username = get_user_input("Enter username: ")
            password = get_user_input("Enter password: ")             # no getpass here
            try:
                login.authenticate_user(username, password)
            except Exception as e:
                print(f"Error during login: {e}")

        elif choice == '3':
            username = get_user_input("Enter username: ")
            new_password = get_user_input("Enter new password: ")     # no getpass here
            confirm_password = get_user_input("Confirm new password: ") # no getpass here
            try:
                login.reset_password(username, new_password, confirm_password)
            except Exception as e:
                print(f"Error during password reset: {e}")

        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
