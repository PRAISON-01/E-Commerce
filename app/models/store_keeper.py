from uuid import UUID, uuid4

from pydantic import EmailStr, Field, BaseModel
from sqlmodel import SQLModel, Field as SQLField


class RegisterStoreKeeper(BaseModel):
    name : str
    email : EmailStr
    password : str = Field(..., min_length=8, max_length=20)

class LoginStoreKeeper(BaseModel):
    email : EmailStr
    password : str = Field(min_length=8, max_length=20)

class LogoutStoreKeeper(BaseModel):
    email : EmailStr


class StoreKeeper(SQLModel, table=True):
    __tablename__ = "store_keepers"
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr = SQLField(unique=True, index=True)
    password: str = Field(..., min_length=8, max_length=20)
    is_logged_in: bool = SQLField(default=False)

class StoreKeeperResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_logged_in: bool
    model_config = {"from_attributes": True}