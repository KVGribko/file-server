from pathlib import Path

from app.config import get_settings
from app.db.models import User


async def create_dir(path: str, user: User) -> Path:
    file_folder = get_settings().FILE_FOLDER
    user_file_folder = file_folder / user.id.hex / path
    user_file_folder.mkdir(parents=True, exist_ok=True)
    return user_file_folder
