from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message()
async def handle_nothing(message: Message):
    text = (
        "⚠️ Ba'zi sabablarga ko'ra bot faoliyatida xattolik yuz. \n Iltimos /start tugmasini bosib botni qayta ishga tushirib yuboring. \n\n"
        "⚠️ По какой-то причине произошла ошибка. Пожалуйста перезапустите бота, нажав кнопку /start. "
    )
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
