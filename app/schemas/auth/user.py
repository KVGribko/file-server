from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    dt_created: datetime
    dt_updated: datetime

    class Config:
        from_attributes = True
