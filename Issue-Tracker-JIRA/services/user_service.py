from fastapi import Depends, HTTPException
from database import get_db
from schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session
import models
from utils.security import hash_password
from auth import get_current_user


def add_user(user, db):
    new_user = models.User(
        name=user.name,
        email=user.email,
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)  
    db.commit()
    db.refresh(new_user)

    return new_user


def delete_user_by_id(user_id, db, current_user_id):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
          
      # Ownership check, The loggod in person can delete himself only (considering he is a user not admin)
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    db.delete(user)
    db.commit()
        
    return {"message": "User deleted successfully", "id": user.id}


def update_user(user_id, user_data, db, current_user_id):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
      # Ownership check
    if current_user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    # Update only provided fields
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.password is not None:
        user.password_hash = hash_password(user_data.password)
    
    db.commit()
    db.refresh(user)
    return user