from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import UserTable
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token

router = APIRouter()

PERMANENT_ADMINS = ["DavidSamson"]

class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "student"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.get("/")
def start():
    return {"message": "Welcome to scholarship portal"}

@router.post("/register", status_code=201)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(UserTable).filter(UserTable.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    if user.username in PERMANENT_ADMINS:
        assigned_role = "admin"
    else:
        assigned_role = "student"
        
    new_user = UserTable(
        username=user.username,
        hashed_password=hash_password(user.password),
        role=assigned_role,
    )
    db.add(new_user)
    db.commit()
    return {"message": f"Account created for {user.username}", "role": assigned_role}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    found = db.query(UserTable).filter(UserTable.username == user.username).first()
    if not found or not verify_password(user.password, found.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "access_token": create_access_token(found.username),
        "token_type": "bearer",
    }