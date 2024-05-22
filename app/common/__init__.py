import typing as t

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.config.database import get_db

DBDepend = t.Annotated[Session, Depends(get_db)]