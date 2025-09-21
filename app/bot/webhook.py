from fastapi import APIRouter, Request, Header, HTTPException
from typing import Any, Dict
from aiogram.types import Update
from app.bot.dispatcher import dp
from app.state import require_state
from app.settings import settings


router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if settings.WEBHOOK_SECRET:
        if x_telegram_bot_api_secret_token != settings.WEBHOOK_SECRET:
            raise HTTPException(status_code=401, detail="Invalid secret token")

    data: Dict[str, Any] = await request.json()
    update = Update.model_validate(data)
    st = require_state()
    await dp.feed_webhook_update(st.bot, update)
    return {"ok": True}
