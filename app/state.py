from dataclasses import dataclass
from aiogram import Bot
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector


@dataclass(slots=True)
class AppState:
    bot: Bot | None = None
    llm: ChatOpenAI | None = None
    emb: OpenAIEmbeddings | None = None
    vs: PGVector | None = None


app_state = AppState()


def require_state() -> AppState:
    if not (app_state.bot and app_state.llm and app_state.emb and app_state.vs):
        raise RuntimeError("App state is not initialized yet")
    return app_state
