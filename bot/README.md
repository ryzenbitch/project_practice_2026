# Dark Machine Telegram Bot

Telegram-бот для проекта **Dark Machine**: справочник по игре, команда, devlog, ресурсы, подписки, обратная связь и мини-викторина.

## Возможности

- `/start` — главное меню проекта.
- `/about` — описание игры и ключевая идея.
- `/paths` — выбор путей развития: Мусорщик / Киборг.
- `/zones` — три уровня завода.
- `/team` — участники и роли.
- `/journal` — журнал разработки.
- `/resources` — полезные ссылки.
- `/subscribe` — подписка на новости проекта.
- `/feedback` — отправка фидбека команде через FSM.
- `/quiz` — мини-викторина по лору.
- `/profile` — профиль пользователя и результат квиза.
- `/status` — проверка доступности сайта через httpx.
- `/admin_stats` — статистика для админов из `ADMIN_IDS`.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`:

```env
BOT_TOKEN=ваш_токен_из_BotFather
DATABASE_URL=sqlite+aiosqlite:///./dark_machine_bot.db
ADMIN_IDS=ваш_telegram_id
PROJECT_SITE_URL=https://example.com
```

## Запуск

```bash
python -m bot.main
```

## Структура

```text
bot/
  main.py              # запуск, роутеры, команды
  config.py            # настройки окружения
  data.py              # контент по игре
  database.py          # async SQLAlchemy engine/session
  models.py            # ORM-модели
  repositories.py      # операции с БД
  keyboards.py         # inline/reply клавиатуры
  handlers/            # команды и callback-логика
  services/http.py     # httpx status-check
```

## Безопасность

Не хардкодьте токен в исходниках. Если токен был отправлен в чат или опубликован, лучше перевыпустить его в @BotFather.
