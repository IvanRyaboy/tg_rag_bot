import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector
from app.settings import settings
from app.logging_config import setup_logging
from app.state import app_state
from app.bot.webhook import router as webhook_router


log = setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if not settings.BOT_TOKEN or not settings.WEBHOOK_URL:
        raise RuntimeError("BOT_TOKEN и WEBHOOK_URL обязательны")
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY обязателен")
    if not settings.PGVECTOR_CONN:
        raise RuntimeError("PGVECTOR_CONN обязателен (postgresql+psycopg://...)")

    app_state.bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    app_state.llm = ChatOpenAI(model=settings.LLM_CHAT_MODEL, base_url=settings.OPENAI_BASE_URL)
    app_state.emb = OpenAIEmbeddings(model=settings.LLM_EMBED_MODEL, base_url=settings.OPENAI_BASE_URL)

    app_state.vs = PGVector(
        embeddings=app_state.emb,
        collection_name="apartments",
        connection=settings.PGVECTOR_CONN,
    )

    try:
        await app_state.bot.set_webhook(url=settings.WEBHOOK_URL, secret_token=settings.WEBHOOK_SECRET or "")
        log.info("Webhook set to %s", settings.WEBHOOK_URL)
        if not settings.SKIP_SET_WEBHOOK:
            await app_state.bot.set_webhook(
                url=settings.WEBHOOK_URL,
                secret_token=settings.WEBHOOK_SECRET or "",
                allowed_updates=Update.all_types(),
            )
            log.info("Webhook set to %s", settings.WEBHOOK_URL)
        else:
            log.info("SKIP_SET_WEBHOOK=true пропускаем установку вебхука")
    except Exception:
        await app_state.bot.session.close()
        raise

    try:
        yield
    finally:
        try:
            await app_state.bot.delete_webhook(drop_pending_updates=False)
            if not settings.SKIP_SET_WEBHOOK:
                await app_state.bot.delete_webhook(drop_pending_updates=False)
        finally:
            await app_state.bot.session.close()
        log.info("Webhook deleted and bot session closed")

app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)


@app.get("/health")
async def health():
    ok = all([app_state.bot, app_state.llm, app_state.emb, app_state.vs])
    return {"ok": ok}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=False)
