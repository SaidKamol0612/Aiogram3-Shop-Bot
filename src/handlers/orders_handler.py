from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.db import db_helper
from core.db.crud import (
    get_user_orders,
    get_products_in_order,
    get_user,
    activate_one_order,
)
from utils import get_data, send_order_to_group
from utils.i18n import get_i18n_msg
from keyboards.reply import back_to_menu, menu_kb
from keyboards.inline import one_order_kb
from states import BotState

router = Router()


@router.callback_query(F.data.startswith("buy_now"))
async def request_one_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Processing...")
    await callback.message.delete_reply_markup()

    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])

    await state.set_state(BotState.waiting_confirm_order)
    await callback.message.answer(
        get_i18n_msg("ask_confirm_one_order", lang),
        reply_markup=one_order_kb(lang, product_id),
    )


@router.callback_query(
    BotState.waiting_confirm_order, F.data.startswith("confirm_one_order")
)
async def confirm_one_order_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Processing...")
    await callback.message.delete_reply_markup()
    await state.set_state(BotState.main)

    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    data = await get_data(lang, data_type="products")
    product = next((p for p in data if p["id"] == product_id), None)

    async with db_helper.session_factory() as session:
        products = [
            {
                "id": product_id,
                "name": product["name"],
                "sku": product["sku"],
                "price": product["price"],
                "count": 1,
            }
        ]

        await activate_one_order(session, user_id, product_id)

        user = await get_user(session, user_id)
        await send_order_to_group(user.name, user.phone_num, products)

    await callback.message.answer(
        get_i18n_msg("order_accepted", lang), reply_markup=menu_kb(lang)
    )


@router.message(F.text.in_(("📦 Mening buyurtmalarim", "📦 Мои заказы")))
async def my_orders(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    user_id = message.from_user.id

    async with db_helper.session_factory() as session:
        orders = await get_user_orders(session, user_id)

    if not orders:
        await message.answer(get_i18n_msg("no_orders", lang))
        return

    response = get_i18n_msg("your_orders", lang)

    async with db_helper.session_factory() as session:
        for order in orders:
            products_id = await get_products_in_order(session, order.id)
            products = [
                p
                for p in (await get_data(lang, data_type="products"))
                if p["id"] in products_id
            ]
            for product in products:
                response += f"\n{product['name']} - {product['price']}\n"

    await message.answer(response, reply_markup=back_to_menu(lang))
