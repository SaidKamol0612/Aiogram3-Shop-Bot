from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from core.db import db_helper
from core.db.crud import get_users
from core.load import get_bot
from core.config import settings
from keyboards.reply import LANG_KB
from states import BotState
from utils.i18n import get_i18n_msg

from handlers import main_router

dp = Dispatcher(storage=MemoryStorage())


async def start_bot() -> None:
    bot = get_bot()

    dp.include_router(main_router)

    await dp.start_polling(bot)


menu_uz = get_i18n_msg("menu", "uz")
menu_ru = get_i18n_msg("menu", "ru")


@dp.message(CommandStart())
@dp.message(F.text.in_((menu_uz[6], menu_ru[6])))
async def cmd_start(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return

    user = message.from_user

    if message.text.startswith("/"):
        msg = (
            f"Salom, <b>{user.first_name}</b>!\n"
            "Iltimos, tilni tanlang.\n\n"
            f"Привет, <b>{user.first_name}</b>!\n"
            "Пожалуйста, выберите язык.\n\n"
        )
    else:
        msg = "Пожалуйста, выберите язык.\n" "Iltimos, tilni tanlang.\n"

    await state.set_state(BotState.choose_lang)
    await message.answer(
        msg,
        reply_markup=LANG_KB,
    )


@dp.message(Command("users"))
async def cmd_users(message: Message):
    if str(message.chat.id) != settings.admin_group.chat_id:
        return

    msg = "👥 Foydalanuvchilar:\n\n"

    async with db_helper.session_factory() as session:
        users = await get_users(session)

    if not users:
        await message.answer("📭 Hech qanday foydalanuvchi topilmadi.")
        return

    for i, user in enumerate(users, 1):
        name = user.name or "Nomaʼlum"
        phone = user.phone_num or "Nomaʼlum"
        username = user.username if user.username else "Nomaʼlum"

        msg += f"👤 {i}. {name} | {phone} | {username}\n"

    msg += f"\n📊 Jami foydalanuvchilar soni: {len(users)}"

    await message.answer(msg)
