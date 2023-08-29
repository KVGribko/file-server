from fastapi import APIRouter, Body, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.connection import get_session
from app.db.models import User
from app.schemas import FileUploadRequest, FileModel, UserFilesModel
from app.utils.user import get_current_user
from app.utils.file import DownloadType


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
async def get_files(
    _: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return None


@api_router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
    response_model=FileModel,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def upload_file(
    _: Request,
    request: FileUploadRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return None


@api_router.get(
    "/download",
    status_code=status.HTTP_200_OK,
    response_model=FileModel,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def get_files(
    _: Request,
    path: str = Query(...),
    type: DownloadType = Query(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return None
