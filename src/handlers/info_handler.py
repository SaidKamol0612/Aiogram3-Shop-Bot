from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.i18n import get_i18n_msg
from states.main_states import BotState
from core.db import db_helper
from core.db.crud import get_user


router = Router()

menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")


@router.message(BotState.main, F.text.in_((menu_uz[4], menu_ru[4])))
async def get_catalog(message: Message, state: FSMContext):
    async with db_helper.session_factory() as session:
        current = await get_user(session, message.from_user.id)
    lang = (await state.get_data()).get("lang")

    info = get_i18n_msg("user_info", lang)
    await message.answer(
        (
            f"<b>{info[0]}</b>: {current.name}\n"
            f"<b>{info[1]}</b>: {current.phone_num}\n"
            f"<b>{info[2]}</b>: {current.username}\n"
        )
    )
