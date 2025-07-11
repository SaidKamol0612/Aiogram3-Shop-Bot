import httpx
import aiohttp

from pathlib import Path

from core.config import settings

MEDIA_DIR = Path(__file__).parent.parent / "media/"


async def login() -> str:
    url = settings.api.login_endpoint
    data = {"login": settings.api.login, "password": settings.api.password}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data["token"]


async def get_products_from_api(lang: str | None = "uz") -> dict:
    langs = {"uz": 1, "ru": 2}
    url = settings.api.products_endpoint

    bearer_token = await login()
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"languageId": langs.get(lang, 1)}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


async def download_image(url, filename="temp_image.png"):
    if not MEDIA_DIR.exists():
        MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = MEDIA_DIR / filename

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_path, "wb") as f:
                    f.write(await response.read())
                return str(file_path)
            else:
                print(f"Ошибка при загрузке: {response.status}")
    return None
