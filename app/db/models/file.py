from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TEXT, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from .base import BaseTable


class FileStorage(BaseTable):
    __tablename__ = "file"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    path = Column(
        TEXT,
        unique=True,
        nullable=False,
    )
    name = Column(
        TEXT,
        nullable=False,
    )
    size = Column(
        INTEGER,
        nullable=False,
    )
    is_downloadable = Column(
        BOOLEAN,
        server_default=expression.true(),
    )
    user = relationship(
        "User",
        back_populates="files",
    )

    def __repr__(self) -> str:
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
