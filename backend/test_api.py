# test_api.py
import requests
import sqlite3
import time

API_URL = "http://127.0.0.1:8000"
DB_PATH = "users.db"  # adjust if your SQLite file is named differently
DB_TIMEOUT = 10  # seconds

users = [
    {"email": "newuser@example.com", "password": "password123"},
    {"email": "user2@example.com", "password": "mypassword"}
]

def cleanup_users():
    """Remove test users safely from the database before running tests."""
    attempt = 0
    while attempt < 5:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT)
            cursor = conn.cursor()
            for user in users:
                cursor.execute("DELETE FROM users WHERE email = ?", (user["email"],))
            conn.commit()
            conn.close()
            print("Cleaned up test users from database.")
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                print(f"Database locked, retrying ({attempt+1}/5)...")
                time.sleep(1)
                attempt += 1
            else:
                raise
    raise Exception("Could not acquire database lock after 5 attempts.")

def signup(user):
    try:
        print(f"\nSignup attempt for {user['email']}:")
        response = requests.post(f"{API_URL}/signup", json=user)
        print("Status code:", response.status_code)
        try:
            print("Response JSON:", response.json())
        except ValueError:
            print("Response text:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def login(user):
    try:
        print(f"\nLogin attempt for {user['email']}:")
        response = requests.post(f"{API_URL}/login", json=user)
        print("Status code:", response.status_code)
        try:
            print("Response JSON:", response.json())
        except ValueError:
            print("Response text:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    cleanup_users()
    for user in users:
        signup(user)
        login(user)
