from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import BotState
from utils.i18n import get_i18n_msg
from core.db import db_helper
from core.db.crud import get_user, set_user
from keyboards.reply import send_phone_kb, menu_kb

router = Router()


@router.message(BotState.choose_lang, F.text)
@router.message(F.text.in_(("🇺🇿 O'zbekcha", "🇷🇺 Русский")))
async def uzbek_language_handler(message: Message, state: FSMContext):
    msg = message.text

    langs = {"🇺🇿 O'zbekcha": "uz", "🇷🇺 Русский": "ru"}
    if langs.__contains__(msg):
        await state.update_data(lang=langs.get(msg))
        await message.answer(get_i18n_msg(msg="chose_lang", lang=langs.get(msg)))
    else:
        await message.answer(
            "⚠️ Iltimos to'gri tilni tanlang.\n⚠️ Пожалуйста выберите правильный язык."
        )
        return

    async with db_helper.session_factory() as session:
        user = await get_user(session, message.from_user.id)

    lang = langs.get(msg)
    if user is None:
        await state.set_state(BotState.waiting_name)
        msg = get_i18n_msg("reg_warning", lang)
        await message.answer(
            f"{msg}\n" + get_i18n_msg("request_name", lang), reply_markup=None
        )
        return

    await state.set_state(BotState.main)
    await message.answer(
        get_i18n_msg("welcome_menu", lang),
        reply_markup=menu_kb(lang),
    )


@router.message(BotState.waiting_name, F.text)
async def get_name(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    await state.update_data(name=message.text)
    await state.set_state(BotState.waiting_phone_num)

    msg = get_i18n_msg("accept_name", lang)
    await message.answer(
        f"{msg}\n" + get_i18n_msg("request_phone", lang),
        reply_markup=send_phone_kb(lang),
    )


@router.message(BotState.waiting_phone_num, F.contact)
async def main_menu(message: Message, state: FSMContext):
    phone_num = (
        message.contact.phone_number
        if message.contact.phone_number.startswith("+")
        else ("+" + message.contact.phone_number)
    )
    name = (await state.get_data()).get("name")
    async with db_helper.session_factory() as session:
        await set_user(
            session,
            tg_id=message.from_user.id,
            username=message.from_user.username,
            name=name,
            phone_num=phone_num,
        )

    lang = (await state.get_data()).get("lang")

    msg = get_i18n_msg("accept_phone", lang)
    msg += "\n" + get_i18n_msg("welcome_menu", lang)

    await state.set_state(BotState.main)
    await message.answer(msg, reply_markup=menu_kb(lang))
