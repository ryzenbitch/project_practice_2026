from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import Settings
from bot.database import Database
from bot.repositories import stats
from bot.services.http import check_url

router = Router(name=__name__)


@router.message(Command("admin_stats"))
async def admin_stats(message: Message, settings: Settings, db: Database) -> None:
    if message.from_user.id not in settings.admin_ids:
        await message.answer("⛔ Команда доступна только администраторам.")
        return
    async with db.session_factory() as session:
        result = await stats(session)
    await message.answer(
        "📊 <b>Статистика бота</b>\n"
        f"Пользователи: <b>{result['users']}</b>\n"
        f"Подписчики: <b>{result['subscribers']}</b>\n"
        f"Фидбек: <b>{result['feedback']}</b>\n"
        f"Попытки квиза: <b>{result['quiz_attempts']}</b>"
    )


@router.message(Command("status"))
async def status(message: Message, settings: Settings) -> None:
    ok, detail = await check_url(settings.project_site_url)
    icon = "🟢" if ok else "🔴"
    await message.answer(f"{icon} <b>Project site status</b>\n{detail}")
