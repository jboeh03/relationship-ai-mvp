import os, datetime, uuid, sqlite3
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB = os.getenv("DATABASE_URL", "app.db")

def init_db():
    conn = sqlite3.connect(DB)
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

app = FastAPI(on_startup=[init_db])

class UserCreate(BaseModel):
    email: str
    password: str

class JournalCreate(BaseModel):
    ciphertext: str
    iv: str

def get_password_hash(p):
    return pwd_context.hash(p)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id,email,password_hash FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if not row: return None
    return {"id": row[0], "email": row[1], "password_hash": row[2]}

@app.post('/signup')
def signup(u: UserCreate):
    if get_user_by_email(u.email):
        raise HTTPException(status_code=400, detail='Email exists')
    uid = str(uuid.uuid4())
    ph = get_password_hash(u.password)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO users (id,email,password_hash,created_at) VALUES (?,?,?,?)", (uid, u.email, ph, datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    token = create_access_token({"sub": uid})
    return {"access_token": token, "token_type": "bearer", "user_id": uid}

@app.post('/token')
def login(form_data: dict):
    # simple form_data expects {'username':..., 'password':...}
    username = form_data.get('username')
    password = form_data.get('password')
    user = get_user_by_email(username)
    if not user or not verify_password(password, user['password_hash']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({"sub": user['id']})
    return {"access_token": token, "token_type": "bearer", "user_id": user['id']}

def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = payload.get('sub')
        return uid
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid auth')

@app.post('/journals')
def save_journal(j: JournalCreate, user_id = Depends(get_current_user)):
    jid = str(uuid.uuid4())
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO journals (id,user_id,ciphertext,iv,created_at) VALUES (?,?,?,?,?)", (jid, user_id, j.ciphertext, j.iv, datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"id": jid, "created_at": datetime.datetime.utcnow().isoformat()}

@app.get('/journals')
def list_journals(user_id = Depends(get_current_user)):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id,ciphertext,iv,created_at FROM journals WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "ciphertext": r[1], "iv": r[2], "created_at": r[3]} for r in rows]

@app.post('/agent/private')
def private_agent(query: dict, user_id = Depends(get_current_user)):
    # Placeholder RAG + model call. DO NOT send unencrypted journals to external APIs without consent.
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    aid = str(uuid.uuid4())
    c.execute("INSERT INTO agent_access_log (id,user_id,agent_name,action,timestamp) VALUES (?,?,?,?,?)", (aid, user_id, 'private_agent', f"queried: {str(query)[:120]}", datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"response": "This is a placeholder response from your private agent. Replace with real model call (Gemini) as needed."}
