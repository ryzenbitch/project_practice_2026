from __future__ import annotations

from aiogram.types import User as TgUser
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Feedback, QuizAttempt, User


async def upsert_user(session: AsyncSession, tg_user: TgUser) -> User:
    result = await session.execute(select(User).where(User.telegram_id == tg_user.id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            telegram_id=tg_user.id,
            username=tg_user.username,
            full_name=tg_user.full_name,
        )
        session.add(user)
    else:
        user.username = tg_user.username
        user.full_name = tg_user.full_name
    await session.commit()
    return user


async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def set_subscription(session: AsyncSession, telegram_id: int, subscribed: bool) -> None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is not None:
        user.is_subscribed = subscribed
        await session.commit()


async def save_feedback(session: AsyncSession, telegram_id: int, category: str, text: str) -> Feedback:
    feedback = Feedback(telegram_id=telegram_id, category=category, text=text)
    session.add(feedback)
    await session.commit()
    return feedback


async def save_quiz_attempt(session: AsyncSession, telegram_id: int, score: int, total: int) -> None:
    session.add(QuizAttempt(telegram_id=telegram_id, score=score, total=total))
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is not None:
        user.quiz_score = max(user.quiz_score, score)
    await session.commit()


async def stats(session: AsyncSession) -> dict[str, int]:
    users = await session.scalar(select(func.count(User.id)))
    subscribers = await session.scalar(select(func.count(User.id)).where(User.is_subscribed.is_(True)))
    feedback_count = await session.scalar(select(func.count(Feedback.id)))
    quiz_attempts = await session.scalar(select(func.count(QuizAttempt.id)))
    return {
        "users": int(users or 0),
        "subscribers": int(subscribers or 0),
        "feedback": int(feedback_count or 0),
        "quiz_attempts": int(quiz_attempts or 0),
    }
