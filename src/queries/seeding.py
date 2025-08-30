from ..app import get_engine
from ..utils.validation import inputs_exist
from ..extensions import Base

def create_table(tablename):
    inputs_exist(tablename)
    if tablename not in Base.metadata.tables:
        raise ValueError(f"Model: {tablename} does not exist!")

    Base.metadata.tables[tablename].create(get_engine(), checkfirst=True)

def drop_table(tablename):
    inputs_exist(tablename)
    if tablename not in Base.metadata.tables:
        raise ValueError(f"Mode: {tablename} does not exist!")

    Base.metadata.tables[tablename].drop(get_engine(), checkfirst=True)
