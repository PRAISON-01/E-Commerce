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

class LogOutStoreKeeper(BaseModel):
    email : EmailStr


class StoreKeeper(SQLModel, table=True):
    __tablename__ = "store_keepers"
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr = SQLField(unique=True, index=True)
    password: str = Field(..., min_length=8, max_length=20)

class StoreKeeperResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    model_config = {"from_attributes": True}