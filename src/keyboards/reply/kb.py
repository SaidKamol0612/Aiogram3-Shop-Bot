from aiogram.utils.keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
)

from utils.i18n import get_i18n_msg

LANG_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 O'zbekcha"),
            KeyboardButton(text="🇷🇺 Русский"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def send_phone_kb(lang: str) -> ReplyKeyboardMarkup:
    msg = get_i18n_msg("send_number", lang)

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=msg, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def menu_kb(lang: str) -> ReplyKeyboardMarkup:
    options = get_i18n_msg("menu", lang)
    kb = ReplyKeyboardBuilder()

    for option in options:
        kb.add(KeyboardButton(text=option))

    return kb.adjust(2).as_markup(resize_keyboard=True)


def back_to_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_i18n_msg("back_to_menu", lang)),
            ],
        ],
        resize_keyboard=True,
    )


def catalog_kb(
    catalog: list, is_ctg: bool = False, lang: str = "uz"
) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    for item in catalog:
        if is_ctg:
            kb.add(KeyboardButton(text=item))
        else:
            kb.add(KeyboardButton(text=f"{item['name']} {item['id']}"))
    if not is_ctg:
        kb.add(KeyboardButton(text=get_i18n_msg("back_to_ctgs", lang)))
    kb.add(KeyboardButton(text=get_i18n_msg("back_to_menu", lang)))

    return kb.adjust(2).as_markup(resize_keyboard=True)
