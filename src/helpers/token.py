from jwt import InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException
from jwt import decode, encode
import dotenv
from datetime import datetime, timedelta

dotenv.load_dotenv()
import os


def verify_token(token: str):
    try:
        decoded_payload = decode(token, os.getenv("JWT_SECRET"), algorithms="HS256")
        return decoded_payload

    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail={"message": "Token has expired"})

    except InvalidTokenError as e:
        raise HTTPException(status_code=400, detail={"mesage": "Invalid token"})


def create_verification_token(user_id: str):
    token = encode(
        {"sub": str(user_id), "exp": datetime.now() + timedelta(hours=1)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token


def create_access_token(user_id: str):
    token = encode(
        {"sub": str(user_id), "exp": datetime.now() + timedelta(days=30)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token


def create_refresh_token(user_id: str):
    token = encode(
        {"sub": str(user_id), "exp": datetime.now() + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token


def create_reset_password_token(user_id: str):
    token = encode(
        {"sub": str(user_id), "exp": datetime.now() + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token
