from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import models

from .user import get_user


async def is_liked(session: AsyncSession, user_tg_id: int, product_id: int) -> bool:
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(models.Favorite).where(
        models.Favorite.product_id == product_id, models.Favorite.user_id == user_id
    )
    res = await session.scalar(stmt)

    return res is not None


async def get_liked_products_id(session: AsyncSession, user_tg_id: int) -> list:
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(models.Favorite).where(models.Favorite.user_id == user_id)
    res = await session.scalars(stmt)

    return [p.product_id for p in res]


async def like_dislike_product(
    session: AsyncSession, user_tg_id: int, product_id: int
) -> bool:
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(models.Favorite).where(
        models.Favorite.user_id == user_id, models.Favorite.product_id == product_id
    )
    res = await session.scalar(stmt)

    if res:
        await session.delete(res)
        await session.commit()
        return False
    like = models.Favorite(user_id=user_id, product_id=product_id)
    session.add(like)
    await session.commit()
    await session.refresh(like)
    return True
