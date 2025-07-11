import os
import uuid

from aiogram import Router, F
from aiogram.types import (
    Message,
    InputMediaPhoto,
    FSInputFile,
    CallbackQuery,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext

from states import BotState
from utils import get_i18n_msg, get_data, download_image, send_order_to_group
from keyboards.inline import product_kb, accept_order_kb
from keyboards.reply import menu_kb
from core.db import db_helper
from core.db.crud import (
    get_products_in_cart,
    is_liked,
    get_count_in_cart,
    remove_product_from_cart,
    add_product_to_cart,
    activate_order,
    get_user,
)

router = Router()

menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")


@router.message(BotState.main, F.text.in_((menu_uz[2], menu_ru[2])))
async def get_favorite(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    user_id = message.from_user.id

    async with db_helper.session_factory() as session:
        cart_products_ids = await get_products_in_cart(session, user_id)
    if not cart_products_ids:
        await message.answer(get_i18n_msg("no_cart_products", lang))
        return

    data = await get_data(lang, "products")
    cart_products = [p for p in data if p["id"] in cart_products_ids]
    await state.set_state(BotState.show_products_in_cart)

    for product in cart_products:
        async with db_helper.session_factory() as session:
            liked_disliked = (
                "❤️\n\n" if await is_liked(session, user_id, product["id"]) else ""
            )

            count_product = await get_count_in_cart(session, user_id, product["id"])

        images = []
        for image in product["images"]:
            filename = await download_image(image["filePath"], f"{uuid.uuid4()}.png")
            images.append(InputMediaPhoto(media=FSInputFile(filename)))

        if len(images) >= 2:
            msg = (await message.answer_media_group(images))[0]
        elif len(images) == 1:
            msg = await message.answer_photo(
                images[0].media, reply_markup=ReplyKeyboardRemove()
            )

        await msg.reply(
            liked_disliked
            + get_i18n_msg("product_details", lang)
            .replace("name", product["name"])
            .replace("price", str(product["price"]))
            .replace("description", product["shortDescription"])
            .replace("count", f"{count_product}"),
            reply_markup=product_kb(product["id"], lang),
        )
        for media in images:
            try:
                os.remove(media.media.path)
            except Exception as e:
                print(f"Ошибка удаления файла: {e}")
    await message.answer(
        get_i18n_msg("request_accept_order", lang), reply_markup=accept_order_kb(lang)
    )


@router.callback_query(BotState.show_products_in_cart, F.data == "confirm_order")
async def accept_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Processing...")
    await callback.message.delete_reply_markup()

    lang = (await state.get_data()).get("lang")
    user_id = callback.from_user.id
    await state.set_state(BotState.main)

    async with db_helper.session_factory() as session:
        product_ids = await get_products_in_cart(session, user_id)
        data = await get_data(lang, "products")
        order = [
            {
                "id": product["id"],
                "name": product["name"],
                "sku": product["sku"],
                "price": product["price"],
                "count": await get_count_in_cart(session, user_id, product["id"]),
            }
            for product in data
            if int(product["id"]) in product_ids
        ]

        await activate_order(session, user_id)

        user = await get_user(session, user_id)
        await send_order_to_group(user.name, user.phone_num, order)

    await callback.message.answer(
        get_i18n_msg("order_accepted", lang), reply_markup=menu_kb(lang)
    )


@router.callback_query(BotState.search_by_code, F.data.startswith("minus_cart"))
@router.callback_query(BotState.show_favorites, F.data.startswith("minus_cart"))
@router.callback_query(BotState.choose_product, F.data.startswith("minus_cart"))
async def minus_from_cart(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    product_id = int(callback.data.split(":")[1])
    user_tg_id = callback.from_user.id

    async with db_helper.session_factory() as session:
        product_count = await get_count_in_cart(session, user_tg_id, product_id)

    if product_count > 0:
        await remove_product_from_cart(session, user_tg_id, product_id)
        product_count -= 1

        pcs = get_i18n_msg("pcs", lang)
        await callback.answer(
            get_i18n_msg("product_removed_from_cart", lang), show_alert=True
        )
        await callback.message.edit_text(
            text=callback.message.text.replace(
                f"{product_count + 1} {pcs}", f"{product_count} {pcs}"
            ),
            reply_markup=product_kb(product_id, lang),
        )

    else:
        await callback.answer(get_i18n_msg("no_product_in_cart", lang), show_alert=True)


@router.callback_query(BotState.show_products_in_cart, F.data.startswith("minus_cart"))
async def minus_from_cart_handler(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    product_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    async with db_helper.session_factory() as session:
        product_count = await get_count_in_cart(session, user_id, product_id)

    if product_count > 1:
        await remove_product_from_cart(session, user_id, product_id)
        product_count -= 1

        pcs = get_i18n_msg("pcs", lang)
        await callback.answer(
            get_i18n_msg("product_removed_from_cart", lang), show_alert=True
        )
        await callback.message.edit_text(
            text=callback.message.text.replace(
                f"{product_count + 1} {pcs}", f"{product_count} {pcs}"
            ),
            reply_markup=product_kb(product_id, lang),
        )
    elif product_count == 1:
        await remove_product_from_cart(session, user_id, product_id)
        await callback.answer(
            get_i18n_msg("product_removed_from_cart", lang), show_alert=True
        )
        await callback.message.delete()
        products = await get_products_in_cart(session, user_id)
        if len(products) == 0:
            await callback.message.answer(get_i18n_msg("no_cart_products", lang))
    else:
        await callback.answer(get_i18n_msg("no_product_in_cart", lang), show_alert=True)


@router.callback_query(BotState.search_by_code, F.data.startswith("add_to_cart"))
@router.callback_query(BotState.show_favorites, F.data.startswith("add_to_cart"))
@router.callback_query(BotState.show_products_in_cart, F.data.startswith("add_to_cart"))
@router.callback_query(BotState.choose_product, F.data.startswith("add_to_cart"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    user_id = callback.from_user.id
    product_id = int(callback.data.split(":")[1])

    async with db_helper.session_factory() as session:
        await add_product_to_cart(session, callback.from_user.id, product_id)
        product_count = await get_count_in_cart(session, user_id, product_id)

    await callback.answer(get_i18n_msg("product_added_to_cart", lang), show_alert=True)
    pcs = get_i18n_msg("pcs", lang)
    await callback.message.edit_text(
        text=callback.message.text.replace(
            f"{product_count - 1} {pcs}", f"{product_count} {pcs}"
        ),
        reply_markup=product_kb(product_id, lang),
    )
