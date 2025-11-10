from aiogram import Bot
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from langchain_postgres import PGVector
from app.state import require_state
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from settings import settings
from dataclasses import dataclass
from typing import AsyncIterator
import os

from app.logging_config import setup_logging

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DATABASE_CONN = os.getenv("PGVECTOR_CONN")
LLM_CHAT_MODEL = os.getenv("LLM_CHAT_MODEL", "gpt-4o-mini")
LLM_EMBED_MODEL = os.getenv("LLM_EMBED_MODEL", "text-embedding-3-small")

log = setup_logging()

app_state = require_state()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if not TOKEN or not WEBHOOK_URL:
        raise RuntimeError("BOT_TOKEN и WEBHOOK_URL обязательны")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY обязателен")

    if not DATABASE_CONN:
        raise RuntimeError("DATABASE_CONN обязателен (postgresql+psycopg://...)")

    app_state.bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app_state.llm = ChatOpenAI(model=LLM_CHAT_MODEL, base_url=OPENAI_BASE_URL)
    app_state.emb = OpenAIEmbeddings(model=LLM_EMBED_MODEL, base_url=OPENAI_BASE_URL)

    app_state.vs = PGVector(
        embeddings=app_state.emb,
        collection_name="apartments",
        connection=DATABASE_CONN,
    )

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


@dataclass(slots=True, frozen=True)
class Resources:
    emb: OpenAIEmbeddings
    vs: PGVector


@asynccontextmanager
async def embed_context(collection_name: str) -> AsyncIterator[Resources]:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY обязателен")
    if not settings.PGVECTOR_CONN:
        raise RuntimeError("PGVECTOR_CONN обязателен (SQLAlchemy URI для langchain_postgres)")

    emb = OpenAIEmbeddings(
        model=settings.LLM_EMBED_MODEL,
        base_url=settings.OPENAI_BASE_URL,
    )

    vs = PGVector(
        embeddings=emb,
        collection_name=collection_name,
        connection=settings.PGVECTOR_CONN,
    )

    res = Resources(emb=emb, vs=vs)
    try:
        yield res
    finally:
        pass
