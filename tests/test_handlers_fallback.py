import importlib
import logging
import pytest
import sys

pytestmark = pytest.mark.asyncio


async def test_non_text_message_logs_and_returns(stub_env, fake_message, caplog, monkeypatch):
    monkeypatch.setitem(sys.modules, "app.llm.rag", type("M", (), {"rag_answer": None}))
    monkeypatch.setitem(sys.modules, "app.utils.text", type("M", (), {"chunk_text": lambda s: [s]}))

    mod = importlib.import_module("app.bot.handlers.fallback")

    caplog.set_level(logging.INFO, logger="tg-webhook")
    msg = fake_message(text=None, content_type="photo")
    await mod.llm_handler(msg)

    assert msg.answers == []
    assert msg.chat.actions == []
    assert any("Non-text message" in r.getMessage() for r in caplog.records)


async def test_success_flow(stub_env, fake_message, monkeypatch):
    monkeypatch.setitem(sys.modules, "app.utils.text", type("M", (), {"chunk_text": lambda s: ["p1", "p2"]}))
    mod = importlib.import_module("app.bot.handlers.fallback")

    async def fake_rag(q: str):
        assert q == "hello"
        return {"answer": "OK", "docs": ["d1", "d2"]}

    monkeypatch.setattr(mod, "rag_answer", fake_rag)

    def chunk_text(s: str):
        assert s == "OK"
        return ["p1", "p2"]
    monkeypatch.setattr(mod, "chunk_text", chunk_text)

    msg = fake_message(text="  hello  ")
    await mod.llm_handler(msg)

    assert msg.chat.actions == ["typing"]
    assert msg.answers == ["p1", "p2"]


@pytest.mark.parametrize("ans", ["", None])
async def test_empty_answer_fallback_to_default(stub_env, fake_message, monkeypatch, ans):
    monkeypatch.setitem(sys.modules, "app.utils.text", type("M", (), {"chunk_text": lambda s: [s]}))
    mod = importlib.import_module("app.bot.handlers.fallback")

    async def fake_rag(_):
        return {"answer": ans, "docs": []}
    monkeypatch.setattr(mod, "rag_answer", fake_rag)

    def chunk_text(s: str):
        assert s == "Введите корректный запрос."
        return [s]
    monkeypatch.setattr(mod, "chunk_text", chunk_text)

    msg = fake_message(text="x")
    await mod.llm_handler(msg)
    assert msg.answers == ["Введите корректный запрос."]


async def test_exception_path(stub_env, fake_message, monkeypatch):
    monkeypatch.setitem(sys.modules, "app.utils.text", type("M", (), {"chunk_text": lambda s: [s]}))
    mod = importlib.import_module("app.bot.handlers.fallback")

    async def failing(_): raise RuntimeError("boom")
    monkeypatch.setattr(mod, "rag_answer", failing)

    msg = fake_message(text="q")
    await mod.llm_handler(msg)
    assert msg.answers == ["Ошибка обработки запроса. Попробуйте позже."]
