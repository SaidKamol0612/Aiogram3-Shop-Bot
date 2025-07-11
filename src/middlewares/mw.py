from typing import Callable, Awaitable, Union, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext


from keyboards.reply import LANG_KB


class UserExistsMiddleware(BaseMiddleware):
    def __init__(self, db_helper, user_getter):
        super().__init__()
        self.db_helper = db_helper
        self.user_getter = user_getter

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], dict], Awaitable],
        event: Union[Message, CallbackQuery],
        data: dict,
    ) -> Awaitable:
        user_id = event.from_user.id
        user_exists = await self.user_exists_in_db(user_id)

        is_start_command = (
            isinstance(event, Message)
            and event.text
            and event.text.startswith("/start")
        )

        if not user_exists and not is_start_command:
            msg = (
                "⚠️ Ba'zi sabablarga ko'ra ro'yxatdan o'tmagan ekansiz.\n"
                "Iltimos, /start buyrug'ini yuboring.\n\n"
                "⚠️ Похоже, что вы не прошли регистрацию.\n"
                "Пожалуйста, сперва зарегистрируйтесь, отправив команду /start."
            )
            if isinstance(event, Message):
                await event.answer(msg, reply_markup=ReplyKeyboardRemove())

            elif isinstance(event, CallbackQuery):
                await event.message.answer(msg, reply_markup=None)
                await event.answer()
            return

        return await handler(event, data)

    async def user_exists_in_db(self, user_id: int) -> bool:
        async with self.db_helper.session_factory() as session:
            user = await self.user_getter(session, user_id)
            return user is not None


class CheckLangMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        fsm_context: FSMContext = data["state"]
        lang = (await fsm_context.get_data()).get("lang")

        if not lang:
            text = "Пожалуйста, выберите язык.\n" "Iltimos, tilni tanlang.\n"
            if isinstance(event, Message):
                await event.answer(
                    text=text,
                    reply_markup=LANG_KB,
                )
                return
            if isinstance(event, CallbackQuery):
                await event.message.answer(
                    text=text,
                    reply_markup=LANG_KB,
                )
                return
        return await handler(event, data)
