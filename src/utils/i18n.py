import json
from pathlib import Path
from typing import Optional

LANGS_PATH = Path(__file__).parent / "langs.json"
_LANG_CACHE: dict = {}


def load_langs():
    global _LANG_CACHE
    if not _LANG_CACHE:
        try:
            with open(LANGS_PATH, "r", encoding="utf-8") as f:
                _LANG_CACHE = json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading language file: {e}")
            _LANG_CACHE = {}
    return _LANG_CACHE


def get_i18n_msg(msg: str, lang: Optional[str] = "uz") -> str:
    langs = load_langs()
    message_dict = langs.get(msg)
    if not message_dict:
        return f"[{msg}]"

    return message_dict.get(lang) or message_dict.get("uz") or f"[{msg}]"
