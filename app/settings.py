from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str
    WEBHOOK_SECRET: str | None = None

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    LLM_CHAT_MODEL: str = "gpt-4o-mini"
    LLM_EMBED_MODEL: str = "text-embedding-3-small"

    PGVECTOR_CONN: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
