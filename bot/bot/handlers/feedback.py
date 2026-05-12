from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database import Database
from bot.keyboards import back_menu, feedback_categories
from bot.repositories import save_feedback, upsert_user

router = Router(name=__name__)


class FeedbackState(StatesGroup):
    waiting_text = State()


@router.message(Command("feedback"))
@router.message(F.text == "💬 Фидбек")
async def feedback_start(message: Message) -> None:
    await message.answer("Выберите категорию фидбека:", reply_markup=feedback_categories())


@router.callback_query(F.data == "feedback:cancel")
async def feedback_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Фидбек отменён.", reply_markup=back_menu())
    await callback.answer()


@router.callback_query(F.data.startswith("feedback:"))
async def feedback_category(callback: CallbackQuery, state: FSMContext) -> None:
    category = callback.data.split(":", 1)[1]
    await state.update_data(category=category)
    await state.set_state(FeedbackState.waiting_text)
    await callback.message.edit_text(
        "Напишите сообщение для команды. Можно описать идею, баг, впечатление от механики или визуала."
    )
    await callback.answer()


@router.message(FeedbackState.waiting_text)
async def feedback_text(message: Message, state: FSMContext, db: Database) -> None:
    data = await state.get_data()
    text = (message.text or "").strip()
    if len(text) < 10:
        await message.answer("Сообщение слишком короткое. Опишите подробнее, минимум 10 символов.")
        return
    async with db.session_factory() as session:
        await upsert_user(session, message.from_user)
        await save_feedback(session, message.from_user.id, data.get("category", "other"), text)
    await state.clear()
    await message.answer("✅ Фидбек сохранён. Спасибо, это попадёт в базу проекта.", reply_markup=back_menu())
