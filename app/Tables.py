from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .SQL_Connection import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = Column(String(50))
    user_email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    create_on = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   


class Note(Base):
    __tablename__ = "notes"
    note_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_title = Column(String(255))
    note_content = Column(String(1000))
    created_on = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"))
   