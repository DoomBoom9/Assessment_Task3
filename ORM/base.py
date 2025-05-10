from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime
try:
    from ORM.ORM_TEST import ORM_session
except ImportError:
    from ORM_TEST import ORM_session

Model = declarative_base()
Model.query = ORM_session.query_property()

class TimeStampedModel(Model):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
