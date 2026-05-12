from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from bot.data import ABOUT, JOURNAL, PATHS, PROJECT, RESOURCES, TEAM, ZONES
from bot.database import Database
from bot.keyboards import COMMANDS_KEYBOARD, back_menu, main_menu, path_menu
from bot.repositories import get_user, set_subscription, upsert_user

router = Router(name=__name__)


def _project_card() -> str:
    return (
        f"<b>{PROJECT['title']}</b>\n"
        f"<i>{PROJECT['tagline']}</i>\n\n"
        f"Жанр: <b>{PROJECT['genre']}</b>\n"
        f"Движок: <b>{PROJECT['engine']}</b>\n"
        f"Длительность: <b>{PROJECT['duration']}</b>\n"
        f"Статус: <b>{PROJECT['status']}</b>\n"
        f"Платформа: <b>{PROJECT['platform']}</b>"
    )


@router.message(CommandStart())
async def start(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        await upsert_user(session, message.from_user)
    await message.answer(
        "🟠 <b>DARK_MACHINE BOT ONLINE</b>\n\n" + _project_card(),
        reply_markup=main_menu(),
    )
    await message.answer("Быстрые кнопки включены.", reply_markup=COMMANDS_KEYBOARD)


@router.callback_query(F.data == "menu:main")
async def menu_main(callback: CallbackQuery) -> None:
    await callback.message.edit_text("🟠 <b>DARK_MACHINE BOT ONLINE</b>\n\n" + _project_card(), reply_markup=main_menu())
    await callback.answer()


@router.message(Command("about"))
@router.message(F.text == "🎮 О проекте")
async def about_command(message: Message) -> None:
    await message.answer(ABOUT, reply_markup=back_menu())


@router.callback_query(F.data == "section:about")
async def about_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(ABOUT, reply_markup=back_menu())
    await callback.answer()


@router.message(Command("paths"))
@router.message(F.text == "⚙️ Пути")
async def paths_command(message: Message) -> None:
    await message.answer("Выберите путь развития героя:", reply_markup=path_menu())


@router.callback_query(F.data == "section:paths")
async def paths_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Выберите путь развития героя:", reply_markup=path_menu())
    await callback.answer()


@router.callback_query(F.data.startswith("path:"))
async def path_detail(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 1)[1]
    path = PATHS[key]
    await callback.message.edit_text(
        f"{path['emoji']} <b>{path['name'].upper()}</b>\n\n{path['text']}",
        reply_markup=path_menu(),
    )
    await callback.answer()


@router.message(Command("zones"))
async def zones_command(message: Message) -> None:
    await message.answer(format_zones(), reply_markup=back_menu())


@router.callback_query(F.data == "section:zones")
async def zones_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(format_zones(), reply_markup=back_menu())
    await callback.answer()


def format_zones() -> str:
    lines = ["🏭 <b>Вертикальная структура завода</b>\n"]
    for idx, zone in enumerate(ZONES, start=1):
        lines.append(f"<b>{idx:02d}. {zone['emoji']} {zone['name']}</b>\n{zone['desc']}")
    return "\n\n".join(lines)


@router.message(Command("team"))
@router.message(F.text == "👥 Команда")
async def team_command(message: Message) -> None:
    await message.answer(format_team(), reply_markup=back_menu())


@router.callback_query(F.data == "section:team")
async def team_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(format_team(), reply_markup=back_menu())
    await callback.answer()


def format_team() -> str:
    lines = ["👥 <b>Команда Dark Machine</b>"]
    for idx, (name, role) in enumerate(TEAM, start=1):
        lines.append(f"<b>{idx:02d}. {name}</b> — {role}")
    return "\n".join(lines)


@router.message(Command("journal"))
@router.message(F.text == "🧾 Журнал")
async def journal_command(message: Message) -> None:
    await message.answer(format_journal(), reply_markup=back_menu())


@router.callback_query(F.data == "section:journal")
async def journal_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(format_journal(), reply_markup=back_menu())
    await callback.answer()


def format_journal() -> str:
    lines = ["🧾 <b>Журнал разработки</b>"]
    for date, title in JOURNAL:
        lines.append(f"<b>{date}</b> — {title}")
    return "\n".join(lines)


@router.message(Command("resources"))
async def resources_command(message: Message) -> None:
    await message.answer(format_resources(), reply_markup=back_menu(), disable_web_page_preview=True)


@router.callback_query(F.data == "section:resources")
async def resources_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(format_resources(), reply_markup=back_menu(), disable_web_page_preview=True)
    await callback.answer()


def format_resources() -> str:
    lines = ["🔗 <b>Ресурсы и референсы</b>"]
    for name, url in RESOURCES:
        lines.append(f"• <a href='{url}'>{name}</a>")
    return "\n".join(lines)


@router.message(Command("subscribe"))
async def subscribe_command(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        await upsert_user(session, message.from_user)
        user = await get_user(session, message.from_user.id)
        new_value = not bool(user and user.is_subscribed)
        await set_subscription(session, message.from_user.id, new_value)
    text = "📡 Подписка на новости включена." if new_value else "📴 Подписка отключена."
    await message.answer(text, reply_markup=back_menu())


@router.callback_query(F.data == "subscribe:toggle")
async def subscribe_callback(callback: CallbackQuery, db: Database) -> None:
    async with db.session_factory() as session:
        await upsert_user(session, callback.from_user)
        user = await get_user(session, callback.from_user.id)
        new_value = not bool(user and user.is_subscribed)
        await set_subscription(session, callback.from_user.id, new_value)
    text = "📡 Подписка на новости включена." if new_value else "📴 Подписка отключена."
    await callback.message.edit_text(text, reply_markup=back_menu())
    await callback.answer()


@router.message(Command("profile"))
async def profile(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        await upsert_user(session, message.from_user)
        user = await get_user(session, message.from_user.id)
    subscribed = "да" if user and user.is_subscribed else "нет"
    score = user.quiz_score if user else 0
    await message.answer(
        f"🧬 <b>Профиль</b>\nID: <code>{message.from_user.id}</code>\nПодписка: <b>{subscribed}</b>\nЛучший квиз-счёт: <b>{score}</b>",
        reply_markup=back_menu(),
    )
