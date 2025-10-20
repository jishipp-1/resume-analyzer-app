from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    email = Column(String(200), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(50), default="candidate")
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    analysis = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="resumes")
