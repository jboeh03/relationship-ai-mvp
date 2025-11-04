# app.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Optional
from database import (
    init_db,
    fetch_user_by_email,
    insert_user
)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------
# Pydantic Models
# ----------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    message: str

# ----------------------
# Utility Functions
# ----------------------
def get_password_hash(password: str) -> str:
    # bcrypt has 72-byte limit, truncate safely
    truncated = password[:72]
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

# ----------------------
# Routes
# ----------------------
@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate):
    existing_user = fetch_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = get_password_hash(user.password)
    insert_user(user.email, password_hash)

    return {"email": user.email, "message": "User created successfully"}

@app.post("/login", response_model=UserResponse)
def login(user: UserCreate):
    db_user = fetch_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"email": user.email, "message": "Login successful"}
