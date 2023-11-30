from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    f_name = Column(String, index=True)
    l_name = Column(String, index=True)
    m_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    token = relationship("Token", back_populates="owner")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="token")


def pas():
    pass