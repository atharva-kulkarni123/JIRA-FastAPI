from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "chnage-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict) -> str:
    encode_to = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_to.update({"exp": expire})

    return jwt.encode(
        encode_to,
        SECRET_KEY,
        ALGORITHM
    )

def create_refresh_token(data: dict) -> str:
    encode_to = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    encode_to.update({"exp": expire, "type": "refresh"})

    return jwt.encode(
        encode_to, 
        SECRET_KEY,
        ALGORITHM
    )
