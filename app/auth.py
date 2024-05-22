import typing as t

from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm 
from starlette import status

from .jwt_manager import create_token


auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", tags=["Login"])
async def login(user: t.Annotated[OAuth2PasswordRequestForm, Depends()]):
    if user.username == "admin@email.com" and user.password == "root":
        token = create_token({"user": user.username})
        response = {"access_token": token, "token_type": "bearer"}
        return response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Credenciales incorrectas"
    )