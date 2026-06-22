from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "chnage-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    encode_to = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_to.update({"exp": expire})

    return jwt.encode(
        encode_to,
        SECRET_KEY,
        ALGORITHM
    )