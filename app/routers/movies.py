import typing as t

from fastapi import APIRouter, HTTPException, Query, Body, Path, Depends
from starlette.responses import Response

from app.common import DBDepend
from app.jwt_manager import validate_token
from app.middlewares.jwt_bearer import JWTBearer 
from app.models.movies import Movies as MoviesModel
from app.schemas.schemas import MoviesSchema, ObjectNotFoundResponse

movies_router = APIRouter()


@movies_router.get("/movies", tags=["Movies"])
async def get_all_movies(db: DBDepend, user = Depends(validate_token)):
    if not user: 
        raise HTTPException(status_code=401, detail="Unauthorized user")

    data = db.query(MoviesModel).all()
    return data


@movies_router.get("/movies/{id}", tags=["Movies"], 
                   dependencies=[Depends(JWTBearer())])
async def get_movie_by_id(db: DBDepend, id: int = Path(ge=1)):
    _movie = db.query(MoviesModel).filter(MoviesModel.id == id).first()
    if _movie is None:    
        return HTTPException(
            status_code=404, 
            detail="Objecto no encontrado"
        )
    return _movie


@movies_router.get("/movies/", tags=["Movies"])
async def get_movies(db: DBDepend, category: t.Optional[str] = Query(default=None)):
    _category = category.lower() if category is not None else None

    if category is not None:
        _movies = db.query(MoviesModel).filter(MoviesModel.category == _category).all()
        return _movies
    else: 
        return []


@movies_router.post("/movies", tags=["Movies"], status_code=201)
async def create_movie(db: DBDepend, data: MoviesSchema = Body()):
    try:
        _movie = MoviesModel(**data.model_dump())
        db.add(_movie)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


@movies_router.put("/movies/{id}", tags=["Movies"],
         responses={200: {"description": "Updated has succesfully"},
                    404: {"description": "Object not found", "model": ObjectNotFoundResponse}})
async def update_movie(db: DBDepend, id: int, data: MoviesSchema = Body()):
    _movie = db.query(MoviesModel).filter(MoviesModel.id == id).first()
    if _movie:
        for name, value in data.model_dump().items():
            setattr(_movie, name, value)
        db.add(_movie)
        db.commit()
    else:
        db.rollback()
        raise HTTPException(status_code=404, detail="Movie not found")


@movies_router.delete("/movies/{id}", tags=["Movies"], 
            responses={204: {"description": "Succesfully operation"}, 
                       404: {"description": "Object not found"}})
async def delete_movie(db: DBDepend, id: int, user = Depends(validate_token)):
    if not user: 
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    _movie = db.query(MoviesModel).filter(MoviesModel.id == id).first()
    if _movie:
        db.delete(_movie)
        db.commit()
        return Response(status_code=204)
    else:
        raise HTTPException(
            status_code=404, 
            detail="Movie not found"
        )

