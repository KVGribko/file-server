from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship

from .base import BaseTable


class User(BaseTable):
    __tablename__ = "user"

    username = Column(
        TEXT,
        nullable=False,
        unique=True,
        index=True,
    )
    password = Column(
        TEXT,
        nullable=False,
        index=True,
    )
    files = relationship(
        "FileStorage",
        back_populates="user",
        cascade="all, delete-orphan",
    )
