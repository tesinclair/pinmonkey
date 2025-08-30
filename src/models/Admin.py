from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import Base

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Admin (id={self.id!r}): Username={self.username!r}"

