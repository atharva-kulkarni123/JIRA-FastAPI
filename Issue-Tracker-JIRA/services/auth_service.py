from fastapi import Depends, HTTPException, status
import models
from utils.auth import create_access_token, create_refresh_token
from utils.security import verify_password
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM

def login(user, db):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    verify = verify_password(user.password, db_user.password_hash)
    if not verify:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = {"sub": str(db_user.id)}
    return {
        "access_token": create_access_token(token), 
        "refresh_token": create_refresh_token(token),
        "token_type": "bearer"
    }

def refresh_access_token(refresh_token, db):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except  JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh Token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh Token")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh Token")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh Token")
    
    token_data = {"sub": str(user.id)}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer"
    }