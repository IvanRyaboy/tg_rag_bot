import importlib
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _purge_app_bot(monkeypatch):
    import sys
    for k in list(sys.modules.keys()):
        if k == "app.bot" or k.startswith("app.bot."):
            monkeypatch.delitem(sys.modules, k, raising=False)


def _make_app(router_module):
    app = FastAPI()
    app.include_router(router_module.router)
    return app


def _valid_update():
    return {"update_id": 1, "message": {"message_id": 10, "text": "hi"}}


def test_webhook_unauthorized(stub_env):
    stub_env["settings_mod"].settings.WEBHOOK_SECRET = "SECRET"
    mod = importlib.import_module("app.bot.webhook")
    app = _make_app(mod)
    client = TestClient(app)

    r = client.post("/webhook", json=_valid_update(),
                    headers={"X-Telegram-Bot-Api-Secret-Token": "WRONG"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid secret token"


def test_webhook_ok_and_dispatch(stub_env):
    stub_env["settings_mod"].settings.WEBHOOK_SECRET = "S"
    mod = importlib.import_module("app.bot.webhook")
    app = _make_app(mod)
    client = TestClient(app)

    r = client.post("/webhook", json=_valid_update(),
                    headers={"X-Telegram-Bot-Api-Secret-Token": "S"})
    assert r.status_code == 200
    assert r.json() == {"ok": True}

    calls = stub_env["calls"]["feed"]
    assert len(calls) == 1
    bot, update = calls[0]
    assert bot == "BOT"
    assert update["validated"] is True


def test_webhook_no_secret_configured_allows_request(stub_env):
    # Пустая строка ⇒ проверка секрета отключена
    stub_env["settings_mod"].settings.WEBHOOK_SECRET = ""
    mod = importlib.import_module("app.bot.webhook")
    app = _make_app(mod)
    client = TestClient(app)

    r = client.post("/webhook", json=_valid_update())
    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_webhook_require_state_failure(stub_env, monkeypatch):
    for k in list(sys.modules.keys()):
        if k == "app.bot.webhook" or k.startswith("app.bot.webhook."):
            monkeypatch.delitem(sys.modules, k, raising=False)

    mod = importlib.import_module("app.bot.webhook")

    def failing_require_state():
        raise RuntimeError("boom")
    monkeypatch.setattr(mod, "require_state", failing_require_state)

    stub_env["settings_mod"].settings.WEBHOOK_SECRET = ""

    from starlette.testclient import TestClient

    app = _make_app(mod)
    client = TestClient(app, raise_server_exceptions=False)  # ключевой флаг

    r = client.post("/webhook", json=_valid_update())
    assert r.status_code == 500

