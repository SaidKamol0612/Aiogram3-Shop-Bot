import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import BotState
from utils import get_i18n_msg, get_data, download_image
from keyboards.inline import product_kb
from keyboards.reply import back_to_menu
from core.db import db_helper
from core.db.crud import (
    get_liked_products_id,
    is_liked,
    get_count_in_cart,
    like_dislike_product,
)

router = Router()

menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")


@router.message(BotState.main, F.text.in_((menu_uz[3], menu_ru[3])))
async def get_favorite(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    user_id = message.from_user.id

    async with db_helper.session_factory() as session:
        liked_ids = await get_liked_products_id(session, user_id)
    if not liked_ids:
        await message.answer(get_i18n_msg("no_favorites", lang))
        return

    data = await get_data(lang, "products")
    favorites = [p for p in data if p["id"] in liked_ids]
    await state.set_state(BotState.show_favorites)

    for product in favorites:
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
                images[0].media, reply_markup=back_to_menu(lang)
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


@router.callback_query(BotState.search_by_code, F.data.startswith("like_dislike"))
@router.callback_query(BotState.main, F.data.startswith("like_dislike"))
@router.callback_query(BotState.choose_product, F.data.startswith("like_dislike"))
async def like_dislike(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])

    async with db_helper.session_factory() as session:
        res = await like_dislike_product(session, callback.from_user.id, product_id)

    if res:
        await callback.answer(get_i18n_msg("liked_unliked", lang)[0], show_alert=True)
    else:
        await callback.answer(get_i18n_msg("liked_unliked", lang)[1], show_alert=True)

    if res:
        msg = "❤️\n\n"
        await callback.message.edit_text(
            (msg + callback.message.text), reply_markup=product_kb(product_id, lang)
        )
    else:
        await callback.message.edit_text(
            callback.message.text.replace("❤️\n\n", ""),
            reply_markup=product_kb(product_id, lang),
        )


@router.callback_query(BotState.show_favorites, F.data.startswith("like_dislike"))
async def like_dislike(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    async with db_helper.session_factory() as session:
        res = await like_dislike_product(session, user_id, product_id)

    if res:
        await callback.answer(get_i18n_msg("liked_unliked", lang)[0], show_alert=True)
    else:
        await callback.answer(get_i18n_msg("liked_unliked", lang)[1], show_alert=True)

    if res:
        msg = "❤️\n\n"
        await callback.message.edit_text(
            (msg + callback.message.text), reply_markup=product_kb(product_id, lang)
        )
    else:
        await callback.message.delete()

        async with db_helper.session_factory() as session:
            liked_ids = await get_liked_products_id(session, user_id)
        if not liked_ids:
            await state.set_state(BotState.main)
            await callback.message.answer(get_i18n_msg("no_favorites", lang))
            return
