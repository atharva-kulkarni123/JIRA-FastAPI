from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from database import get_db
from sqlalchemy.orm import Session
from utils.auth import SECRET_KEY, ALGORITHM
import models

security = HTTPBearer()

def get_current_user(credentials=Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid Token"
            )
    except JWTError:
        raise HTTPException(
                status_code=401, detail="Invalid Token"
            )
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not Found"
        )
    return user