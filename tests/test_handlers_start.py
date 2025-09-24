import importlib
import logging
import pytest
import sys

pytestmark = pytest.mark.asyncio


async def test_start_handler_logs_and_answers(stub_env, fake_message, caplog, monkeypatch):
    monkeypatch.setitem(sys.modules, "aiogram.filters", type("M", (), {"CommandStart": lambda *a, **k: object()}))

    mod = importlib.import_module("app.bot.handlers.start")

    caplog.set_level(logging.INFO, logger="tg-webhook")
    msg = fake_message(text="/start")
    await mod.command_start_handler(msg)

    assert any("Start from user_id=" in r.getMessage() for r in caplog.records)
    assert msg.answers == ["Отправьте вопрос — я отвечу, опираясь на контекст."]
