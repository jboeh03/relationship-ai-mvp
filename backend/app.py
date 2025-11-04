# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from passlib.context import CryptContext

# --------------------------
# Models
# --------------------------
class User(BaseModel):
    email: str
    password: str

# --------------------------
# App & CORS
# --------------------------
app = FastAPI()

origins = [
    "https://relationship-ai-mvp.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Password hashing
# --------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # truncate to 72 bytes for bcrypt
    truncated = password[:72]
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)

# --------------------------
# Database setup
# --------------------------
DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --------------------------
# Routes
# --------------------------
@app.get("/")
def root():
    return {"message": "Backend is live!"}

@app.post("/signup")
def signup(user: User):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if email exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = get_password_hash(user.password)
    cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (user.email, password_hash)
    )
    conn.commit()
    conn.close()
    return {"email": user.email, "message": "User created successfully"}

@app.post("/login")
def login(user: User):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    _, email, password_hash = db_user
    if not verify_password(user.password, password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"email": email, "message": "Login successful"}
