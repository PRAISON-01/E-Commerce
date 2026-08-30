from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr
from sqlmodel import SQLModel, Field as SQLField


class Customer(SQLModel, table=True):

    __tablename__ = "customers"


    id:  UUID= SQLField(default_factory=uuid4, primary_key=True)
    name: str= SQLField(min_length=3, max_length=20)
    email:EmailStr = SQLField(unique=True, index=True)
    password: str = SQLField(..., min_length=8, max_length=20)

class RegisterCustomer(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length = 8, max_length = 20)

class LoginCustomer(BaseModel):
    email: EmailStr
    password: str

class LogoutCustomer(BaseModel):
    email: EmailStr

class CustomerResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}
