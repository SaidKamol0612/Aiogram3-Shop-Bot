from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import models

from .user import get_user


async def get_user_active_cart(session: AsyncSession, user_tg_id: int) -> models.Cart:
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(models.Cart).where(
        models.Cart.user_id == user_id, models.Cart.is_ordered.is_(False)
    )
    return await session.scalar(stmt)


async def get_count_in_cart(
    session: AsyncSession, user_tg_id: int, product_id: int
) -> int:
    user_id = (await get_user(session, user_tg_id)).id

    cart = await get_user_active_cart(session, user_tg_id)

    stmt = select(models.ProductCart).where(
        models.ProductCart.product_id == product_id,
        models.ProductCart.user_id == user_id,
    )
    if cart:
        stmt = stmt.where(models.ProductCart.cart_id == cart.id)
    res = await session.scalar(stmt)

    return res.product_count if res else 0


async def get_products_in_cart(session: AsyncSession, user_tg_id: int) -> list:
    cart = await get_user_active_cart(session, user_tg_id)
    if not cart:
        return []

    stmt = select(models.ProductCart).where(models.ProductCart.cart_id == cart.id)
    res = await session.scalars(stmt)

    return [p.product_id for p in res]


async def get_user_orders(session: AsyncSession, user_tg_id: int) -> list:
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(models.Cart).where(
        models.Cart.is_ordered.is_(True), models.Cart.user_id == user_id
    )
    res = await session.scalars(stmt)

    return [order for order in res]


async def get_order(session: AsyncSession, order_id: int):
    stmt = select(models.Cart).where(models.Cart.id == order_id)
    res = await session.scalar(stmt)

    return res


async def get_products_in_order(session: AsyncSession, order_id: int) -> list:
    stmt = select(models.ProductCart).where(models.ProductCart.cart_id == order_id)
    res = await session.scalars(stmt)

    return [p.product_id for p in res]


async def remove_product_from_cart(
    session: AsyncSession, user_tg_id: int, product_id: int
) -> None:
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(models.ProductCart).where(
        models.ProductCart.user_id == user_id,
        models.ProductCart.product_id == product_id,
    )
    product_cart = await session.scalar(stmt)

    product_cart.product_count -= 1
    if product_cart.product_count == 0:
        await session.delete(product_cart)
        await session.commit()
        return

    await session.commit()
    await session.refresh(product_cart)


async def add_product_to_cart(
    session: AsyncSession, user_tg_id: int, product_id: int
) -> None:
    user_id = (await get_user(session, user_tg_id)).id

    cart = await get_user_active_cart(session, user_tg_id)
    if not cart:
        cart = models.Cart(user_id=user_id, is_ordered=False)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
    else:
        stmt = select(models.ProductCart).where(
            models.ProductCart.cart_id == cart.id,
            models.ProductCart.product_id == product_id,
        )
        product_cart = await session.scalar(stmt)

        if not product_cart:
            product_cart = models.ProductCart(
                cart_id=cart.id, user_id=user_id, product_id=product_id, product_count=1
            )
            session.add(product_cart)
            await session.commit()
            await session.refresh(product_cart)
        else:
            product_cart.product_count += 1
            await session.commit()
            await session.refresh(product_cart)


async def activate_order(session: AsyncSession, user_tg_id: int) -> None:
    cart = await get_user_active_cart(session, user_tg_id)
    cart.is_ordered = True
    await session.commit()
    await session.refresh(cart)


async def activate_one_order(
    session: AsyncSession, user_tg_id: int, product_id: int
) -> None:
    user_id = (await get_user(session, user_tg_id)).id

    cart = models.Cart(user_id=user_id, is_ordered=True)
    session.add(cart)
    await session.commit()
    await session.refresh(cart)

    product_cart = models.ProductCart(
        cart_id=cart.id, user_id=user_id, product_id=product_id, product_count=1
    )
    session.add(product_cart)
    await session.commit()
    await session.refresh(product_cart)
