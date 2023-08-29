from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.exc import UnknownHashError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .database import get_user
from app.config import get_settings
from app.db.connection import get_session
from app.db.models import User
from app.schemas import TokenData


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> User | bool:
    user = await get_user(session, username)
    if not user:
        return False
    return user if verify_password(password, user.password) else False


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    settings = get_settings()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    pwd_context = get_settings().PWD_CONTEXT
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(get_settings().OAUTH2_SCHEME),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            get_settings().SECRET_KEY,
            algorithms=[get_settings().ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e
    user = await get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
