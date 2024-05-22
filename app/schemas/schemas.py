from datetime import datetime

from pydantic import BaseModel, Field


class MoviesSchema(BaseModel):
    id: int | None = None 
    title: str = Field(min_length=3, max_length=20)
    overview: str = Field(min_length=3, max_length=50)
    year: int = Field(le=datetime.now().year)
    rating: float = Field(gt=1, lt=10)
    category: str = Field(min_length=4, max_length=10)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 0,
                "title": "Título prueba",
                "overview": "Descripción de prueba",
                "year": datetime.now().year,
                "rating": 9.7,
                "category": "Comedia"
            }
        }


class UsersSchema(BaseModel):
    email: str
    password: str


class ObjectNotFoundResponse(BaseModel):
    status_code: int
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 404,
                "message": "Objecto no encontrado"
            }
        }