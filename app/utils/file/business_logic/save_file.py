from pathlib import Path

import aiofiles
from fastapi import UploadFile

from .create_dir import create_dir
from app.db.models import User


async def save_file_on_disk(file: UploadFile, path: str, user: User) -> Path:
    user_file_folder = await create_dir(path, user)
    file_path = user_file_folder / file.filename
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file.file.read())
    return file_path
