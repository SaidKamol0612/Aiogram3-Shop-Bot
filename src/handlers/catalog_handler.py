import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import BotState
from utils import get_i18n_msg, get_data, download_image, get_item
from keyboards.reply import catalog_kb
from keyboards.inline import product_kb
from core.db import db_helper
from core.db.crud import is_liked, get_count_in_cart, like_dislike_product

router = Router()

menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")

BACK_TO_CTGS = ("🔙 Kategoriyalarga qaytish.", "🔙 Вернуться к категориям.")


@router.message(BotState.main, F.text.in_((menu_uz[1], menu_ru[1])))
@router.message(BotState.choose_product, F.text.in_(BACK_TO_CTGS))
async def get_catalog(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    ctgs = await get_data(lang)

    await state.set_state(BotState.choose_ctg)
    await message.answer(
        get_i18n_msg("categories", lang),
        reply_markup=catalog_kb(ctgs, is_ctg=True, lang=lang),
    )


@router.message(BotState.choose_ctg, F.text)
async def get_products(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    ctgs = await get_data(lang)
    if message.text in ctgs:
        products = await get_data(lang, data_type="products")
        ctg_products = [
            ctg_product
            for ctg_product in products
            if ctg_product["category"] == message.text
        ]

        await state.set_state(BotState.choose_product)
        await message.answer(
            get_i18n_msg("ctg_products", lang),
            reply_markup=catalog_kb(ctg_products, lang=lang),
        )
    else:
        await message.answer(get_i18n_msg("ctg_not_found", lang))


@router.message(BotState.choose_product, F.text)
async def get_product(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    product_id = message.text.split(" ")[-1]
    user_id = message.from_user.id

    data = await get_data(lang, "products")
    product = get_item(product_id, data)

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
