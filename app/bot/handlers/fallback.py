import time, logging
from aiogram.types import Message
from app.bot.dispatcher import dp
from app.llm.rag import rag_answer
from app.utils.text import chunk_text


log = logging.getLogger("tg-webhook")


@dp.message()
async def llm_handler(message: Message) -> None:
    if not message.text:
        log.info(
            "Non-text message chat_id=%s user_id=%s content_type=%s",
            message.chat.id,
            message.from_user.id if message.from_user else None,
            message.content_type,
        )
        return

    user_q = message.text.strip()
    t0 = time.perf_counter()
    try:
        await message.chat.do("typing")
        result = await rag_answer(user_q)
        latency_ms = int((time.perf_counter() - t0) * 1000)

        answer = result["answer"] or "Введите корректный запрос."
        docs = result["docs"]

        log.info(
            "LLM OK: chat_id=%s user_id=%s ms=%d q=%r -> a.len=%d | sources=%d",
            message.chat.id,
            message.from_user.id if message.from_user else None,
            latency_ms,
            user_q,
            len(answer),
            len(docs),
        )

        for part in chunk_text(answer):
            await message.answer(part)

    except Exception as e:
        log.exception("LLM ERROR: chat_id=%s user_id=%s q=%r err=%s",
                      message.chat.id,
                      message.from_user.id if message.from_user else None,
                      user_q, e)
        await message.answer("Ошибка обработки запроса. Попробуйте позже.")
