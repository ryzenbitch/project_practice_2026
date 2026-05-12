from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _parse_admin_ids(raw: str | None) -> FrozenSet[int]:
    if not raw:
        return frozenset()
    ids: set[int] = set()
    for item in raw.replace(";", ",").split(","):
        item = item.strip()
        if item.isdigit():
            ids.add(int(item))
    return frozenset(ids)


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str
    admin_ids: FrozenSet[int]
    project_site_url: str


def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "PASTE_YOUR_TOKEN_HERE":
        raise RuntimeError("BOT_TOKEN is not set. Put your Telegram bot token into .env")

    return Settings(
        bot_token=token,
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dark_machine_bot.db"),
        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS")),
        project_site_url=os.getenv("PROJECT_SITE_URL", "https://example.com").strip(),
    )
