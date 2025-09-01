from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

def db_init(uri: str):
    engine = create_engine(uri, echo=True, future=True)
    Session = sessionmaker(engine)

    from .models import Item
    Base.metadata.create_all(engine)

    return Session, engine
