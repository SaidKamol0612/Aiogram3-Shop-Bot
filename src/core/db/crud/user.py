from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import models


async def get_users(session: AsyncSession) -> list:
    stmt = select(models.User)
    res = await session.scalars(stmt)

    return [u for u in res]


async def get_user(session: AsyncSession, tg_id: int) -> models.User | None:
    stmt = select(models.User).where(models.User.tg_id == tg_id)
    res = await session.scalar(stmt)

    return res or None


async def set_user(
    session: AsyncSession, tg_id: int, username: str, name: str, phone_num: str
) -> None:
    new_user = models.User(
        tg_id=tg_id,
        name=name,
        phone_num=phone_num,
        username=("@" + username) if username else None,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
