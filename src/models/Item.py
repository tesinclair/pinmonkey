from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from ..extensions import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    title: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Item (id={self.id!r}): Image Link={self.img!r}, Price={self.price!r}, Title={self.title!r}."
