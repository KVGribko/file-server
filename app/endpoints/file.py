from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.connection import get_session
from app.db.models import User
from app.schemas import FileModel, UserFilesModel
from app.utils.file import DownloadType, create_file_in_db, get_file, save_file_on_disk
from app.utils.user import get_current_user


api_router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


@api_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserFilesModel,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def get_files_info(
    _: Request,
    current_user: User = Depends(get_current_user),
):
    return UserFilesModel(account_id=current_user.id, files=current_user.files)


@api_router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
    response_model=FileModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters:",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def upload_file(
    _: Request,
    path: str = Body(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        file_path = await save_file_on_disk(file, path, current_user)
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    return await create_file_in_db(session, current_user, file, str(file_path))


@api_router.get(
    "/download",
    status_code=status.HTTP_200_OK,
    response_model=FileModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters:",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "File not found",
        },
    },
)
async def download_file(
    _: Request,
    path: str = Query(...),
    type: DownloadType = Query(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        file = await get_file(session, path, type)
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    if file:
        return FileResponse(
            file.path,
            media_type="application/octet-stream",
            filename=file.name,
        )
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail=f"File with {str(type)}={path} not found",
    )
