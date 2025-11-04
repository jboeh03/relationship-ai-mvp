from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Dict

app = FastAPI()

# In-memory user store (replace with DB in production)
users_db: Dict[str, Dict] = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class User(BaseModel):
    email: str
    password: str

# Utility functions
def get_password_hash(password: str) -> str:
    truncated = password[:72]  # bcrypt max length
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)

# Signup endpoint
@app.post("/signup")
async def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = get_password_hash(user.password)
    users_db[user.email] = {"email": user.email, "password_hash": password_hash}
    return {"email": user.email, "message": "User created successfully"}

# Login endpoint
@app.post("/login")
async def login(user: User):
    if user.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    stored = users_db[user.email]
    if verify_password(user.password, stored["password_hash"]):
        return {"email": user.email, "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
