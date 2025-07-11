from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    tg_id = mapped_column(BigInteger())
    username: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    phone_num: Mapped[str] = mapped_column(String)
