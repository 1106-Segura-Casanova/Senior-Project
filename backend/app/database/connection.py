# Purpose: Set up the database connection.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#SQLAlchemy Engine Creation API https://docs.sqlalchemy.org/en/20/core/engines.html
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# SessionLocal = sessionmaker(...) from FastAPI https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/database.py#L11
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

# def get_db() function from FastAPI https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/main.py#L15-L20
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()