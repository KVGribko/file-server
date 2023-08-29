from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import FileStorage, User


async def create_file_in_db(
    session: AsyncSession,
    user: User,
    file: UploadFile,
    file_path: Path,
) -> FileStorage:
    new_file = FileStorage(
        user_id=user.id,
        path=file_path,
        name=file.filename,
        size=int(file.size),
    )
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file
