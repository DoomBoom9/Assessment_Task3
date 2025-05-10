import os
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{BASE_DIR}/db.db', echo=True)

ORM_session = scoped_session(
    sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine
    )
)

@event.listens_for(Engine,"connect")
def set_sqlite_pragma(dbapi_con, connection_record):
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
