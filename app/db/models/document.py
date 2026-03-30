# app/db/models/document.py

from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)