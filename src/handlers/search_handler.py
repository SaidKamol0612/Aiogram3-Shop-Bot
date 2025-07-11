import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from states import BotState
from utils import get_i18n_msg, get_data, download_image
from keyboards.reply import back_to_menu
from keyboards.inline import product_kb
from core.db import db_helper
from core.db.crud import is_liked, get_count_in_cart

router = Router()

menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")


@router.message(BotState.main, F.text.in_((menu_uz[0], menu_ru[0])))
async def search_by_code(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    await state.set_state(BotState.search_by_code)
    await message.answer(
        get_i18n_msg("request_code", lang), reply_markup=back_to_menu(lang)
    )


@router.message(BotState.search_by_code, F.text)
async def get_product_by_code(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    user_id = message.from_user.id
    code = message.text.strip()

    products = await get_data(lang, "products")
    product = next((p for p in products if str(p["sku"]) == code), None)

    if product:
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
            msg = await message.answer_photo(images[0].media)

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
    else:
        await message.answer(get_i18n_msg("product_not_found", lang))
