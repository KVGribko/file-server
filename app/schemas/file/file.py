from datetime import datetime

from pydantic import UUID4, BaseModel


class FileModel(BaseModel):
    id: UUID4
    path: str
    name: str
    size: int
    is_downloadable: bool
    dt_created: datetime
    dt_updated: datetime

    class Config:
        from_attributes = True


class UserFilesModel(BaseModel):
    account_id: UUID4
    files: list[FileModel]
