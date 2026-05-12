from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data import PATHS, QUIZ


def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎮 О проекте", callback_data="section:about")
    builder.button(text="⚙️ Пути", callback_data="section:paths")
    builder.button(text="🏭 Зоны", callback_data="section:zones")
    builder.button(text="👥 Команда", callback_data="section:team")
    builder.button(text="🧾 Журнал", callback_data="section:journal")
    builder.button(text="🔗 Ресурсы", callback_data="section:resources")
    builder.button(text="🧪 Викторина", callback_data="quiz:start")
    builder.button(text="📡 Подписка", callback_data="subscribe:toggle")
    builder.adjust(2)
    return builder.as_markup()


def path_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{PATHS['scavenger']['emoji']} Мусорщик", callback_data="path:scavenger")],
        [InlineKeyboardButton(text=f"{PATHS['cyborg']['emoji']} Киборг", callback_data="path:cyborg")],
        [InlineKeyboardButton(text="← Назад", callback_data="menu:main")],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="← Главное меню", callback_data="menu:main")]])


def feedback_categories() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Геймплей", callback_data="feedback:gameplay")],
        [InlineKeyboardButton(text="🎨 Арт / UI", callback_data="feedback:art")],
        [InlineKeyboardButton(text="📖 Сюжет / лор", callback_data="feedback:lore")],
        [InlineKeyboardButton(text="🐞 Баг", callback_data="feedback:bug")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="feedback:cancel")],
    ])


def quiz_question(index: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for option_index, option in enumerate(QUIZ[index]["options"]):
        builder.button(text=option, callback_data=f"quiz:answer:{index}:{option_index}")
    builder.adjust(1)
    return builder.as_markup()


COMMANDS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 О проекте"), KeyboardButton(text="⚙️ Пути")],
        [KeyboardButton(text="👥 Команда"), KeyboardButton(text="🧾 Журнал")],
        [KeyboardButton(text="🧪 Викторина"), KeyboardButton(text="💬 Фидбек")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите раздел Dark Machine",
)
