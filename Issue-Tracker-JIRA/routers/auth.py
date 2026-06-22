from fastapi import APIRouter, Depends, HTTPException
from schemas import LoginResponse 
from database import get_db
from sqlalchemy.orm import Session
import models
from utils.security import verify_password
from utils.auth import create_access_token
from auth import get_current_user

router = APIRouter(prefix="/auth", tags = ["auth"])

@router.post("/login")
def login(user: LoginResponse, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    verify = verify_password(user.password, db_user.password_hash)

    if not verify:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token(
        {"sub": str(db_user.id)}
    )

    return {
        "access_token": token, 
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email    
    }