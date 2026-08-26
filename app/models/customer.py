from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr
from sqlmodel import SQLModel, Field as SQLField


class Customer(SQLModel, table=True):
    id:  UUID= SQLField(default_factory=uuid4, primary_key=True)
    name: str= Field(min_length=3, max_length=20)
    email:EmailStr = SQLField(unique=True, index=True)
    password: str = Field(min_length=8, max_length=20)

class RegisterCustomer(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str

class LoginCustomer(BaseModel):
    id: int
    email: str
    password: str

class LogoutCustomer(BaseModel):
    email: str