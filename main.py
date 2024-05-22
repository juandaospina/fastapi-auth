from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers.movies import movies_router    
from app.auth import auth_router
from app.config.database import Base, engine
from app.middlewares.error_handler import ErrorHandler
from app.models import movies  

app = FastAPI(
    title="Curso FastAPI básico de platzi",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Home"])
def root():
    return RedirectResponse("/docs")

# Routers
app.include_router(movies_router, prefix="/v1")
app.include_router(auth_router, prefix="/v1")

# Middlewares
app.add_middleware(ErrorHandler)


