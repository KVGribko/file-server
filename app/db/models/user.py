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
        lazy="selectin",
    )

    def __repr__(self) -> str:
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
