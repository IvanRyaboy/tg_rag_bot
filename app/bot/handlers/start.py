from aiogram.filters import CommandStart
from aiogram.types import Message
from app.bot.dispatcher import dp
import logging


log = logging.getLogger("tg-webhook")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    log.info(
        "Start from user_id=%s, name=%s, username=%s",
        message.from_user.id if message.from_user else None,
        message.from_user.full_name if message.from_user else None,
        message.from_user.username if message.from_user else None,
    )
    await message.answer("Отправьте вопрос — я отвечу, опираясь на контекст.")
