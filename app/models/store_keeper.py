from pydantic import EmailStr
from pydantic.v1 import BaseModel


class RegisterStoreKeeper(BaseModel):
    name : str
    email : EmailStr
    