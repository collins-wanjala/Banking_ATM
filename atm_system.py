import json
import os
import getpass
import sys
from datetime import datetime

USERS_DIR = "users"

# Ensure users folder exists
if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)


def get_user_file(username):
    return os.path.join(USERS_DIR, f"{username}.json")


def get_transaction_file(username):
    return os.path.join(USERS_DIR, f"{username}_transactions.txt")


def save_user_data(username, data):
    with open(get_user_file(username), 'w') as f:
        json.dump(data, f)


def load_user_data(username):
    with open(get_user_file(username), 'r') as f:
        return json.load(f)


def log_transaction(username, action, amount, account="Main"):
    with open(get_transaction_file(username), "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {action} ${amount:.2f} in {account} Account\n")


def create_account():
    print("\n=== Create New Account ===")
    username = input("Choose a username: ").strip()
    if os.path.exists(get_user_file(username)):
        print("Username already exists. Try another one.\n")
        return

    password = getpass.getpass("Create a password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match.\n")
        return

    data = {
        "password": password,
        "main_balance": 1000.0,
        "savings_balance": 500.0
    }

    save_user_data(username, data)
    print(f"Account '{username}' created successfully!\n")


def login():
    print("\n=== Login ===")
    username = input("Username: ").strip()
    if not os.path.exists(get_user_file(username)):
        print("Account does not exist.\n")
        return None

    password = getpass.getpass("Password: ")
    user_data = load_user_data(username)
    if password != user_data['password']:
        print("Incorrect password.\n")
        return None

    print(f"Welcome, {username}!\n")
    return username


def show_menu():
    print("==== ATM MAIN MENU ====")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transfer to Savings")
    print("5. Change Password")
    print("6. View Transaction History")
    print("7. Logout")


def check_balance(user_data):
    print(f"\nMain Account Balance: ${user_data['main_balance']:.2f}")
    print(f"Savings Account Balance: ${user_data['savings_balance']:.2f}\n")


def deposit(username, user_data):
    try:
        amount = float(input("Enter amount to deposit into Main Account: $"))
        if amount <= 0:
            print("Amount must be greater than zero.\n")
            return
        user_data["main_balance"] += amount
        log_transaction(username, "Deposit", amount)
        print(f"${amount:.2f} deposited successfully.\n")
    except ValueError:
        print("Invalid input.\n")


def withdraw(username, user_data):
    try:
        amount = float(input("Enter amount to withdraw: $"))
        if amount <= 0:
            print("Amount must be greater than zero.\n")
        elif amount > user_data["main_balance"]:
            print("Insufficient balance.\n")
        else:
            user_data["main_balance"] -= amount
            log_transaction(username, "Withdraw", amount)
            print(f"${amount:.2f} withdrawn successfully.\n")
    except ValueError:
        print("Invalid input.\n")


def transfer(username, user_data):
    try:
        amount = float(input("Enter amount to transfer to Savings: $"))
        if amount <= 0:
            print("Amount must be greater than zero.\n")
        elif amount > user_data["main_balance"]:
            print("Insufficient funds.\n")
        else:
            user_data["main_balance"] -= amount
            user_data["savings_balance"] += amount
            log_transaction(username, "Transfer to Savings", amount, "Main")
            log_transaction(username, "Transfer from Main", amount, "Savings")
            print(f"${amount:.2f} transferred to savings.\n")
    except ValueError:
        print("Invalid input.\n")


def change_password(username, user_data):
    old = getpass.getpass("Enter current password: ")
    if old != user_data["password"]:
        print("Incorrect password.\n")
        return

    new = getpass.getpass("New password: ")
    confirm = getpass.getpass("Confirm new password: ")
    if new != confirm:
        print("Passwords do not match.\n")
        return

    user_data["password"] = new
    print("Password changed successfully.\n")


def view_transaction_history(username):
    print("\n==== Transaction History ====")
    try:
        with open(get_transaction_file(username), "r") as f:
            history = f.read()
            print(history if history else "No transactions yet.")
    except FileNotFoundError:
        print("No transactions found.")
    print()


def user_session(username):
    while True:
        user_data = load_user_data(username)
        show_menu()
        choice = input("Choose an option (1-7): ")

        if choice == '1':
            check_balance(user_data)
        elif choice == '2':
            deposit(username, user_data)
        elif choice == '3':
            withdraw(username, user_data)
        elif choice == '4':
            transfer(username, user_data)
        elif choice == '5':
            change_password(username, user_data)
        elif choice == '6':
            view_transaction_history(username)
        elif choice == '7':
            print(f"Goodbye, {username}!\n")
            save_user_data(username, user_data)
            break
        else:
            print("Invalid option. Choose between 1 and 7.\n")


def main():
    while True:
        print("==== CLI BANK ====")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")

        choice = input("Select an option (1-3): ").strip()
        if choice == '1':
            username = login()
            if username:
                user_session(username)
        elif choice == '2':
            create_account()
        elif choice == '3':
            print("Exiting system. Goodbye!")
            sys.exit()
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
