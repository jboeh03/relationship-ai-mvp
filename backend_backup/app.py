from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import init_db, create_user, get_user_by_email, log_agent_action

# Initialize database
init_db()

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------
# Pydantic models
# -------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# -------------------------------
# Helper functions
# -------------------------------
def get_password_hash(password: str) -> str:
    # truncate to 72 bytes for bcrypt
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

# -------------------------------
# Routes
# -------------------------------
@app.post("/signup")
def signup(user: UserCreate):
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = get_password_hash(user.password)
    user_id = create_user(user.email, password_hash)
    return {"id": user_id, "email": user.email}

@app.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"id": db_user["id"], "email": db_user["email"]}

# Example endpoint to log agent actions
@app.post("/log_agent_action")
def log_action(user_id: str, agent_name: str, action: str):
    log_agent_action(user_id, agent_name, action)
    return {"status": "logged"}
