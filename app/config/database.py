from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base  

sqlite_file_name = "./database.sqlite"
db_url = f"sqlite:///{sqlite_file_name}"

# Define de engine
engine = create_engine(db_url, echo=True)

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = None
    try:
        db = Session()
        yield db        
    finally:
        if db is not None:
            db.close()