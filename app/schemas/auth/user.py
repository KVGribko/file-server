from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True
