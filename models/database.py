from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker


# # postgres connection
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:deno0707@localhost:5432/techtutor"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


# SQLite connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()