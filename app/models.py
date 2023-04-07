import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    firstname = Column(String, default='default firstname from models not reached')
    password = Column(String)
    is_active = Column(Boolean, default=True)
    age = Column(Integer, default=18)
    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, firstname={self.firstname})>"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    count = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # users.id -TABLENAME
    created_at = Column(String, default=datetime.datetime.utcnow())
