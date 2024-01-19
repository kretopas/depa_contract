# app/auth/auth_handler.py

import time
import jwt
from typing import Dict
from decouple import config

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
ACCESS_EXPIRED_TIME = config("JWT_ACCESS_EXPIRED", cast=int)
REFRESH_EXPIRED_TIME = config("JWT_REFRESH_EXPIRED", cast=int)

def create_access_token(user_id: str, user_group: int, username: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "user_group": user_group,
        "username": username,
        "expires": time.time() + ACCESS_EXPIRED_TIME
	}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def create_refresh_token(user_id: str, user_group: int, username: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "user_group": user_group,
        "username": username,
        "expires": time.time() + REFRESH_EXPIRED_TIME
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}