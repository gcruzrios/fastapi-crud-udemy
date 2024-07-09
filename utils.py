import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any, Dict
from jose import jwt
#
import time
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# ACCESS_TOKEN_EXPIRE_MINUTES = 900  # 600 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
# ALGORITHM = "HS256"
# JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
# JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: str) -> Dict[str,str]:
    # if expires_delta is not None:

    #     expires_delta = datetime.utcnow() + expires_delta
    #     #expires_delta = datetime.now(UTC) + expires_delta
    #     print('If way!')
        
    # else:
    #     expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #     print("else way")

    payload = {
        "user_id": subject,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    #to_encode = {"exp": expires_delta, "sub": str(subject)}
    #encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return token

