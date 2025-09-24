import pytest
from types import SimpleNamespace


def test_require_state_uninitialized(monkeypatch):
    import app.state as state
    state.app_state.bot = None
    state.app_state.llm = None
    state.app_state.emb = None
    state.app_state.vs = None

    with pytest.raises(RuntimeError, match="App state is not initialized yet"):
        state.require_state()


def test_require_state_initialized():
    import app.state as state
    state.app_state.bot = SimpleNamespace()
    state.app_state.llm = SimpleNamespace()
    state.app_state.emb = SimpleNamespace()
    state.app_state.vs = SimpleNamespace()

    s = state.require_state()
    assert s is state.app_state
