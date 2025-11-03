import sqlite3
conn = sqlite3.connect("app.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at TEXT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS journals (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    ciphertext TEXT,
    iv TEXT,
    created_at TEXT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS agent_access_log (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    agent_name TEXT,
    action TEXT,
    timestamp TEXT
)""")
conn.commit()
conn.close()
print('Initialized app.db')