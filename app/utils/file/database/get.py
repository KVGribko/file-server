from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import FileStorage
from app.utils.file.enum import DownloadType


async def get_file(session: AsyncSession, path: str, type: DownloadType) -> FileStorage:
    query = select(FileStorage).where(getattr(FileStorage, type) == path)
    file = await session.execute(query)
    return file.scalar_one_or_none()
