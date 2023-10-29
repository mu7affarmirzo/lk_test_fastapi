# schemas.py
from pydantic import BaseModel


class LoginForm(BaseModel):
    msisdn: str
    password: str


class UserCreate(BaseModel):
    phone_number: str
    f_name: str
    l_name: str
    m_name: str
    password: str


class User(BaseModel):
    id: int
    phone_number: str
    f_name: str
    l_name: str
    m_name: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    f_name: str
    l_name: str
    m_name: str
