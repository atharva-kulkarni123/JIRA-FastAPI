from fastapi import APIRouter, Depends, HTTPException, status
from schemas import LoginRequest 
from database import get_db
from sqlalchemy.orm import Session
import models
from utils.security import verify_password
from utils.auth import create_access_token, create_refresh_token
from auth import get_current_user
from utils.auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from services import auth_service

router = APIRouter(prefix="/auth", tags = ["auth"])

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(user, db)

@router.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(refresh_token, db)

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email    
    }