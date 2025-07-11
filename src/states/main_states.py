from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    choose_lang = State()

    # Registration states
    waiting_name = State()
    waiting_phone_num = State()

    # Menu states
    main = State()
    search_by_code = State()
    show_favorites = State()
    show_products_in_cart = State()

    # Catalog states
    choose_ctg = State()
    choose_product = State()
    waiting_confirm_order = State()
