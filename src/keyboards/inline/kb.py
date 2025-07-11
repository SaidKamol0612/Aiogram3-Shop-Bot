from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.i18n import get_i18n_msg


def product_kb(product_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    product_menu = get_i18n_msg("product_menu", lang)

    kb.add(
        InlineKeyboardButton(
            text=product_menu[0], callback_data=f"like_dislike:{product_id}"
        ),
        InlineKeyboardButton(
            text=product_menu[1], callback_data=f"buy_now:{product_id}"
        ),
        InlineKeyboardButton(
            text=product_menu[2], callback_data=f"minus_cart:{product_id}"
        ),
        InlineKeyboardButton(
            text=product_menu[3], callback_data=f"add_to_cart:{product_id}"
        ),
    )

    return kb.adjust(2).as_markup()


def accept_order_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_i18n_msg("yes", lang), callback_data="confirm_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_i18n_msg("back_to_menu", lang),
                    callback_data="back_to_menu",
                )
            ],
        ]
    )


def one_order_kb(lang: str, product_id: int) -> InlineKeyboardMarkup:
    confirm_text = get_i18n_msg("confirm_one_order", lang)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=confirm_text, callback_data=f"confirm_one_order:{product_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_i18n_msg("back_to_menu", lang),
                    callback_data="back_to_menu",
                ),
            ],
        ],
        resize_keyboard=True,
    )
