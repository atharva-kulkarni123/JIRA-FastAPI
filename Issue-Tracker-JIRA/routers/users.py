from fastapi import Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserUpdate
import models
from utils.security import hash_password
from auth import get_current_user
from services import user_service

router = APIRouter(prefix = "/user", tags = ["users"])

@router.get("/all", response_model=list[UserResponse])
def get_all_users(current_user = Depends(get_current_user), db: Session= Depends(get_db)):
    return db.query(models.User).all()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.add_user(user, db)

@router.delete("/delete")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.delete_user_by_id(user_id, db, current_user.id)

@router.patch("/update/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.update_user(user_id, user_data, db, current_user.id)