from datetime import datetime, timedelta
import jwt

SECRET_KEY = "me gustan los ravioles"
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
