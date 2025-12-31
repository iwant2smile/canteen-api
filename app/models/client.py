from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True, unique=True)