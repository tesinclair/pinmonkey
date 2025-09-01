from ..utils.validation import inputs_exist
from ..extensions import Base

def create_table(engine, tablename):
    inputs_exist(engine, tablename)
    if tablename not in Base.metadata.tables:
        raise ValueError(f"Model: {tablename} does not exist!")

    Base.metadata.tables[tablename].create(engine, checkfirst=True)

def drop_table(engine, tablename):
    inputs_exist(engine, tablename)
    if tablename not in Base.metadata.tables:
        raise ValueError(f"Mode: {tablename} does not exist!")

    Base.metadata.tables[tablename].drop(engine, checkfirst=True)
