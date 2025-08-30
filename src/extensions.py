from sqlalchemy import create_engine, DeclarativeBase
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass

db_init(uri: str):
    engine = create_engine(uri, echo=True, future=True)
    Session = sessionmaker(engine)

    from .models import Item
    Base.metadata.create_all(engine)

    return Session, engine

