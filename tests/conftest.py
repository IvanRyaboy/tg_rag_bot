import pytest


# Фейки для Aiogram
class FakeChat:
    def __init__(self, chat_id: int):
        self.id = chat_id
        self.actions = []

    async def do(self, action: str):
        self.actions.append(action)


class FakeUser:
    def __init__(self, user_id: int, full_name="User Name", username="user"):
        self.id = user_id
        self.full_name = full_name
        self.username = username


class FakeMessage:
    def __init__(self, text: str | None, chat_id=100, user_id=200, content_type="text"):
        self.text = text
        self.chat = FakeChat(chat_id)
        self.from_user = FakeUser(user_id)
        self.content_type = content_type
        self._answers = []

    async def answer(self, text: str):
        self._answers.append(text)

    @property
    def answers(self):
        return list(self._answers)


@pytest.fixture
def fake_message():
    return FakeMessage


# Заготовка окружения
@pytest.fixture
def stub_env(monkeypatch):
    import sys, types

    settings_mod = types.SimpleNamespace(
        settings=types.SimpleNamespace(WEBHOOK_SECRET="")
    )
    monkeypatch.setitem(sys.modules, "app.settings", settings_mod)

    state_mod = types.SimpleNamespace(
        require_state=lambda: types.SimpleNamespace(bot="BOT")
    )
    monkeypatch.setitem(sys.modules, "app.state", state_mod)

    calls = {"feed": []}

    async def fake_feed(bot, update):
        calls["feed"].append((bot, update))

    def noop_decorator(*a, **k):
        def wrap(f): return f
        return wrap

    monkeypatch.setitem(
        sys.modules,
        "app.bot.dispatcher",
        types.SimpleNamespace(dp=types.SimpleNamespace(
            feed_webhook_update=fake_feed,
            message=noop_decorator,
        )),
    )

    class UpdateStub:
        @classmethod
        def model_validate(cls, data):
            return {"validated": True, **data}

    class MessageStub:
        pass

    aiogram_pkg = types.ModuleType("aiogram")
    types_mod = types.ModuleType("aiogram.types")
    setattr(types_mod, "Update", UpdateStub)
    setattr(types_mod, "Message", MessageStub)

    monkeypatch.setitem(sys.modules, "aiogram", aiogram_pkg)
    monkeypatch.setitem(sys.modules, "aiogram.types", types_mod)

    filters_mod = types.ModuleType("aiogram.filters")

    class CommandStart:
        def __init__(self, *args, **kwargs):
            pass
    setattr(filters_mod, "CommandStart", CommandStart)
    monkeypatch.setitem(sys.modules, "aiogram.filters", filters_mod)

    return {"calls": calls, "settings_mod": settings_mod}

