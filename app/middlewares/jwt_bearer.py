from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from app.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["user"] != "admin@email.com":
            raise HTTPException(status_code=403)
        return data