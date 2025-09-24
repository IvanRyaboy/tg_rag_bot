from types import SimpleNamespace
from app.llm.prompt import build_prompt


def test_build_prompt_includes_docs_and_query():
    docs = [
        SimpleNamespace(page_content="desc A", metadata={"apartment_id": 1, "total_area": 50, "price": 10000000}),
        SimpleNamespace(page_content="desc B", metadata={"apartment_id": 2}),
    ]
    q = "сколько стоит метр"
    prompt = build_prompt(q, docs)

    assert "desc A" in prompt
    assert "desc B" in prompt
    assert "apartment_id" in prompt
    assert q in prompt


def test_build_prompt_with_empty_docs_has_placeholder():
    prompt = build_prompt("q", [])
    assert "контекст не предоставлен" in prompt
