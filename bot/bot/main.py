from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import BotCommand, ErrorEvent, Message

from bot.config import Settings, get_settings
from bot.database import Database
from bot.handlers import admin, common, feedback, quiz


KNOWN_COMMANDS = {
    "start", "about", "paths", "zones", "team", "journal",
    "resources", "quiz", "feedback", "profile", "subscribe",
    "status", "admin_stats", "cancel",
}


def is_unknown_slash_command(message: Message) -> bool:
    if not message.text or not message.text.startswith("/"):
        return False

    command = message.text.split()[0].split("@", 1)[0].lstrip("/").lower()
    return command not in KNOWN_COMMANDS


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="about", description="О проекте"),
        BotCommand(command="paths", description="Пути развития"),
        BotCommand(command="zones", description="Зоны завода"),
        BotCommand(command="team", description="Команда"),
        BotCommand(command="journal", description="Журнал разработки"),
        BotCommand(command="resources", description="Ресурсы и референсы"),
        BotCommand(command="quiz", description="Мини-викторина"),
        BotCommand(command="feedback", description="Отправить фидбек"),
        BotCommand(command="profile", description="Профиль"),
        BotCommand(command="subscribe", description="Включить/выключить подписку"),
        BotCommand(command="status", description="Проверка сайта"),
    ])


async def on_error(event: ErrorEvent) -> None:
    logging.exception("Update processing failed", exc_info=event.exception)


async def unknown_command(message: Message) -> None:
    await message.answer("Команда не распознана. Используйте /start, чтобы открыть меню.")


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings: Settings = get_settings()
    db = Database(settings)
    await db.init()

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(settings=settings, db=db)

    dp.include_router(common.router)
    dp.include_router(feedback.router)
    dp.include_router(quiz.router)
    dp.include_router(admin.router)
    dp.errors.register(on_error)
    dp.message.register(unknown_command, is_unknown_slash_command)

    await set_commands(bot)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        await db.dispose()


if __name__ == "__main__":
    asyncio.run(main())
