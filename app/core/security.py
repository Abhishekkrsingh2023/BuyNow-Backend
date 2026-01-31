from datetime import datetime, timedelta, timezone
from typing import Optional
from app.config.settings import settings
from jwt import PyJWTError
import jwt
import bcrypt

# creates the JWT token
async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    create_access_token
    
    :param data: Description: provide data to be encoded in the token
    :type data: dict
    :param expires_delta: Description: time duration for token expiration
    :type expires_delta: Optional[timedelta]
    :return: Description: encoded JWT token
    :rtype: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    create_refresh_token
    
    :param data: Description: provide data to be encoded in the token
    :type data: dict
    :param expires_delta: Description: time duration for token expiration
    :type expires_delta: Optional[timedelta]
    :return: Description: encoded JWT refresh token
    :rtype: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=30)  # Default 30 days for refresh token
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

# verifies the JWT token
async def verify_access_token(token: str) -> dict:
    """
    verify_access_token verifies the JWT access token
    
    :param token: Description: JWT token to be verified
    :type token: str
    :return: Description: payload extracted from the token if valid
    :rtype: dict
    """
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    # incase of invalid token
    except PyJWTError as e:
        return None

async def verify_refresh_token(token: str) -> dict:
    """
    verify_refresh_token verifies the JWT refresh token
    
    :param token: Description: JWT refresh token to be verified
    :type token: str
    :return: Description: payload extracted from the token if valid
    :rtype: dict
    """
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    # incase of invalid token
    except PyJWTError as e:
        return None


# password hashing and verification
async def hash_password(plain_password: str) -> str:
    """
    hash_password
    
    :param plain_password: Description: plain text password to be hashed
    :type plain_password: str
    :return: Description: hashed password
    :rtype: str
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    verify_password
    
    :param plain_password: Description: plain text password to verify
    :type plain_password: str
    :param hashed_password: Description: hashed password to compare against
    :type hashed_password: str
    :return: Description: True if passwords match, False otherwise
    :rtype: bool
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

