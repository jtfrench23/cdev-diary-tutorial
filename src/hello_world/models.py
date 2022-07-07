from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

import sqlalchemy_aurora_data_api

sqlalchemy_aurora_data_api.register_dialects()

Base = declarative_base()

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300))
    content = Column(String(500))
    
    def __repr__(self):
        return f"Content(id={self.id!r}, title={self.title!r}, content={self.content!r})"