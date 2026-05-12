from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.data import QUIZ
from bot.database import Database
from bot.keyboards import back_menu, quiz_question
from bot.repositories import save_quiz_attempt, upsert_user

router = Router(name=__name__)


class QuizState(StatesGroup):
    in_progress = State()


async def send_question(target: Message, index: int, score: int) -> None:
    item = QUIZ[index]
    await target.answer(
        f"🧪 <b>Викторина Dark Machine</b>\n"
        f"Вопрос {index + 1}/{len(QUIZ)} · счёт {score}\n\n"
        f"{item['question']}",
        reply_markup=quiz_question(index),
    )


@router.message(Command("quiz"))
@router.message(F.text == "🧪 Викторина")
async def quiz_start_message(message: Message, state: FSMContext) -> None:
    await state.set_state(QuizState.in_progress)
    await state.update_data(score=0)
    await send_question(message, index=0, score=0)


@router.callback_query(F.data == "quiz:start")
async def quiz_start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(QuizState.in_progress)
    await state.update_data(score=0)
    await callback.message.answer("Запускаю мини-викторину по лору.")
    await send_question(callback.message, index=0, score=0)
    await callback.answer()


@router.callback_query(QuizState.in_progress, F.data.startswith("quiz:answer:"))
async def quiz_answer(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    _, _, raw_index, raw_answer = callback.data.split(":")
    index = int(raw_index)
    answer = int(raw_answer)
    data = await state.get_data()
    score = int(data.get("score", 0))
    correct = answer == QUIZ[index]["answer"]
    if correct:
        score += 1
    next_index = index + 1
    await callback.answer("Верно!" if correct else "Не совсем.")

    if next_index >= len(QUIZ):
        await state.clear()
        async with db.session_factory() as session:
            await upsert_user(session, callback.from_user)
            await save_quiz_attempt(session, callback.from_user.id, score, len(QUIZ))
        await callback.message.answer(
            f"🏁 <b>Квиз завершён</b>\nРезультат: <b>{score}/{len(QUIZ)}</b>",
            reply_markup=back_menu(),
        )
        return

    await state.update_data(score=score)
    await send_question(callback.message, index=next_index, score=score)
