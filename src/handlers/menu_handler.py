from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import BotState
from utils import get_i18n_msg
from keyboards.reply import menu_kb

router = Router()

menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")

BACK_TO_MENU = ("🏠 Bosh menyuga qaytish.", "🏠 Вернуться в главоному меню.")


@router.message(F.text.in_(BACK_TO_MENU))
async def main_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    await state.set_state(BotState.main)
    await message.answer(get_i18n_msg("welcome_menu", lang), reply_markup=menu_kb(lang))


@router.callback_query(F.data == "back_to_menu")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    await callback.answer("Menu")
    await state.set_state(BotState.main)
    await callback.message.answer(
        get_i18n_msg("welcome_menu", lang), reply_markup=menu_kb(lang)
    )
