import bcrypt
import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30    
REFRESH_TOKEN_EXPIRE_DAYS = 7

def get_hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    # Convert password to bytes and hash
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Return as string for database storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False
    
def create_access_token(data: dict)-> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None