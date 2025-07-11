from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import settings

_BOT: Bot | None = None


def _start() -> Bot:
    global _BOT
    _BOT = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    return _BOT


def get_bot() -> Bot:
    global _BOT
    if _BOT is None:
        _BOT = _start()
    return _BOT
