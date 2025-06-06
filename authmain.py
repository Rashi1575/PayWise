import signup
import login
import psycopg2

def get_user_input(prompt):
    return input(prompt).strip()

if __name__ == "_main_":
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
        conn = psycopg2.connect(
            host="db.havcrxnjjopcwjhtiytp.supabase.co",   # Paste Supabase Host here
            database="paywise_db",     # Database name
            user="rashi",         # Username
            password="CodeBlooded00@",  # Your Supabase DB password
            port=5432                # Port
        )