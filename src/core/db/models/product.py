from sqlalchemy import ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


from .base import Base
from .user import User


class Favorite(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    product_id: Mapped[int]


class Cart(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    is_ordered: Mapped[bool]


class ProductCart(Base):
    cart_id: Mapped[int] = mapped_column(ForeignKey(Cart.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    product_id: Mapped[int]
    product_count: Mapped[int]
