import logging
import asyncio

from bot import start_bot
from core import settings
from core.db import db_helper


async def run():
    await db_helper.init_db()

    try:
        await start_bot()
    except:
        print("Bot stopped.")
    finally:
        await db_helper.dispose()


if __name__ == "__main__":
    logging.basicConfig(
        filename=settings.logging.log_file,
        format=settings.logging.log_format,
        datefmt=settings.logging.log_date_format,
        level=settings.logging.log_level_value,
    )

    asyncio.run(run())
