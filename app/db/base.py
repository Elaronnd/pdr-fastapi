from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)
from app.config.config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_ADDRESS,
    DB_PORT,
    DB_NAME
)

engine = create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}', echo=True)

class Base(DeclarativeBase):
    ...

Session = sessionmaker(engine)

def create_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)