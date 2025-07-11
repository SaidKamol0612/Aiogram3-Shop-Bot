__all__ = ("main_router",)

from aiogram import Router

from middlewares import UserExistsMiddleware, CheckLangMiddleware
from core.db import db_helper
from core.db.crud import get_user

from .reg_handler import router as reg_router
from .menu_handler import router as menu_router
from .search_handler import router as search_router
from .catalog_handler import router as catalog_router
from .cart_handler import router as cart_router
from .favorites_handler import router as favorites_router
from .info_handler import router as info_router
from .orders_handler import router as orders_router
from .help_router import router as help_router

main_router = Router()
user_exists = UserExistsMiddleware(db_helper, get_user)
check_lang = CheckLangMiddleware()


# Function-Helper
def apply_middlewares(router: Router, *middlewares):
    for middleware in middlewares:
        router.message.middleware(middleware)
        router.callback_query.middleware(middleware)


# Apply middlewares
apply_middlewares(menu_router, user_exists, check_lang)
apply_middlewares(search_router, user_exists, check_lang)
apply_middlewares(catalog_router, user_exists, check_lang)
apply_middlewares(cart_router, user_exists, check_lang)
apply_middlewares(favorites_router, user_exists, check_lang)
apply_middlewares(info_router, user_exists, check_lang)
apply_middlewares(orders_router, user_exists, check_lang)

# Including routers
main_router.include_router(reg_router)
main_router.include_router(menu_router)
main_router.include_router(search_router)
main_router.include_router(catalog_router)
main_router.include_router(cart_router)
main_router.include_router(favorites_router)
main_router.include_router(info_router)
main_router.include_router(orders_router)
main_router.include_router(help_router)
