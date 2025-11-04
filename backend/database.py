import sqlite3
from typing import Optional
from datetime import datetime
import uuid

DB_FILE = "app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    # Journals table
    c.execute("""
        CREATE TABLE IF NOT EXISTS journals (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            ciphertext TEXT,
            iv TEXT,
            created_at TEXT NOT NULL
        )
    """)
    # Agent access log table
    c.execute("""
        CREATE TABLE IF NOT EXISTS agent_access_log (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            agent_name TEXT,
            action TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print('Initialized app.db')

def create_user(email: str, password_hash: str) -> str:
    """Create a new user and return their ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    c.execute("""
        INSERT INTO users (id, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, email, password_hash, created_at))
    conn.commit()
    conn.close()
    return user_id

def get_user_by_email(email: str) -> Optional[dict]:
    """Fetch user by email."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, email, password_hash, created_at FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "created_at": row[3]
        }
    return None

def log_agent_action(user_id: str, agent_name: str, action: str):
    """Log agent actions."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    log_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    c.execute("""
        INSERT INTO agent_access_log (id, user_id, agent_name, action, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (log_id, user_id, agent_name, action, timestamp))
    conn.commit()
    conn.close()
