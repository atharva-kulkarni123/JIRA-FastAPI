from fastapi import Depends, HTTPException, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserUpdate
import models
from utils.security import hash_password

router = APIRouter(prefix = "/user", tags = ["users"])

@router.get("/all", response_model=list[UserResponse])
def get_all_users(db: Session= Depends(get_db)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=404, detail="No Users registered")
    else:
        return user

@router.post("/register")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
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

@router.delete("/delete")
def delete_user_by_name(name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
          
    db.delete(user)
    db.commit()
        
    return {"message": "User deleted successfully", "name": name}

@router.patch("/update/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
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