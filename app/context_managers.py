from aiogram import Bot
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from langchain_postgres import PGVector
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DATABASE_CONN = os.getenv("PGVECTOR_CONN")
LLM_CHAT_MODEL = os.getenv("LLM_CHAT_MODEL", "gpt-4o-mini")
LLM_EMBED_MODEL = os.getenv("LLM_EMBED_MODEL", "text-embedding-3-small")


class AppState:
    bot: Bot
    llm: ChatOpenAI
    emb: OpenAIEmbeddings
    vs: PGVector


app_state = AppState()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if not TOKEN or not WEBHOOK_URL:
        raise RuntimeError("BOT_TOKEN и WEBHOOK_URL обязательны")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY обязателен")

    if not DATABASE_CONN:
        raise RuntimeError("DATABASE_CONN обязателен (postgresql+psycopg://...)")

    # 1) Инициализируем бота
    app_state.bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # 2) Инициализируем LLM/Embeddings
    app_state.llm = ChatOpenAI(model=LLM_CHAT_MODEL, base_url=OPENAI_BASE_URL)
    app_state.emb = OpenAIEmbeddings(model=LLM_EMBED_MODEL, base_url=OPENAI_BASE_URL)

    # 3) Инициализируем векторное хранилище
    app_state.vs = PGVector(
        embeddings=app_state.emb,
        collection_name="apartments",
        connection=DATABASE_CONN,
    )

    # 5) Регистрируем вебхук
    try:
        await app_state.bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
        log.info("Webhook set to %s", WEBHOOK_URL)
    except Exception:
        await app_state.bot.session.close()
        raise

    try:
        yield
    finally:
        try:
            await app_state.bot.delete_webhook(drop_pending_updates=False)
        finally:
            await app_state.bot.session.close()
        log.info("Webhook deleted and bot session closed")