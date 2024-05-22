import os
import typing as t
from datetime import datetime, timedelta, timezone

from jwt import encode, decode, PyJWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


def create_token(payload: dict) -> str:
    payload.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=20)})
    _key = os.environ.get("SECRET_SIGN")
    token = encode(payload, _key, algorithm="HS256")
    return token

def validate_token(token: t.Annotated[str, Depends(oauth_scheme)]) -> dict:
    try:
        payload = decode(token, os.environ.get("SECRET_SIGN"), algorithms=["HS256"])
        user = payload.get("user")

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized user")

        return {"user": user}
    except PyJWTError as jwt_error:
        print(jwt_error)
        raise HTTPException(status_code=401, detail="Unauthorized user")