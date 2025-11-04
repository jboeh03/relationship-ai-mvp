# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3
import time

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_PATH = "users.db"
DB_TIMEOUT = 10  # seconds
DB_RETRIES = 5   # number of retries if locked

# Pydantic models
class User(BaseModel):
    email: str
    password: str

# Helper functions
def get_password_hash(password: str) -> str:
    # bcrypt only supports max 72 bytes
    truncated = password[:72]
    return pwd_context.hash(truncated)

def get_db_connection():
    """Return a SQLite connection with timeout and retry if locked."""
    attempt = 0
    while attempt < DB_RETRIES:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT)
            return conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                attempt += 1
                time.sleep(1)
            else:
                raise
    raise Exception("Could not acquire database connection after retries")

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Routes
@app.post("/signup")
def signup(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = get_password_hash(user.password)

    # Insert new user safely
    attempt = 0
    while attempt < DB_RETRIES:
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (user.email, password_hash)
            )
            conn.commit()
            conn.close()
            return {"email": user.email, "message": "User created successfully"}
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                attempt += 1
                time.sleep(1)
            else:
                conn.close()
                raise
    conn.close()
    raise HTTPException(status_code=500, detail="Database is locked, try again later")

@app.post("/login")
def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (user.email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password_hash = row[0]
    truncated_password = user.password[:72]  # bcrypt max 72 bytes
    if not pwd_context.verify(truncated_password, stored_password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"email": user.email, "message": "Login successful"}
