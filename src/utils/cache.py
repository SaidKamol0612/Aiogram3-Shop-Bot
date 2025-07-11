import json

from datetime import datetime, timedelta
from pathlib import Path

from .api import get_products_from_api

CACHE_PATH = Path(__file__).parent / "cache.json"


def _is_stale_json():
    if not CACHE_PATH.exists():
        return True

    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_at = data.get("updated_at")
    if not updated_at:
        return True

    try:
        updated_at = datetime.fromisoformat(updated_at)
        if datetime.now() - updated_at > timedelta(days=1):
            return True
    except ValueError:
        return True


async def _get_new_data():
    data_uz = await get_products_from_api("uz")
    data_ru = await get_products_from_api("ru")
    updated_at = datetime.now().isoformat()

    categories_uz = [product["category"] for product in data_uz]
    categories_ru = [product["category"] for product in data_ru]

    return {
        "updated_at": updated_at,
        "data": {
            "uz": {"categories": list(set(categories_uz)), "products": data_uz},
            "ru": {"categories": list(set(categories_ru)), "products": data_ru},
        },
    }


async def get_data(lang: str = "uz", data_type: str = "categories") -> dict:
    if _is_stale_json():
        data = await _get_new_data()

        with open(CACHE_PATH, "w") as f:
            json.dump(data, f)
    else:
        with open(CACHE_PATH, "r") as f:
            data = json.load(f)
    return data.get("data").get(lang).get(data_type)
