from uuid import UUID, uuid4
from pydantic import EmailStr, Field, BaseModel
from sqlmodel import SQLModel, Field as SQLField

from enums.user_role import UserRole


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr = SQLField(unique=True, index=True)
    password: str = Field(..., min_length=8, max_length=20)
    role: UserRole
    is_logged_in: bool = SQLField(default=False)

class RegisterUser(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class LogoutUser(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: UserRole
    is_logged_in: bool

    model_config = {"from_attributes": True}