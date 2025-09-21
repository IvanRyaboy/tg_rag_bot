import asyncio
from typing import Any, Dict, List
from langchain.schema import Document
from app.state import require_state
from .prompt import build_prompt


async def rag_answer(query: str) -> Dict[str, Any]:
    st = require_state()
    docs: List[Document] = await asyncio.to_thread(st.vs.similarity_search, query, 4)
    prompt = build_prompt(query, docs)
    resp = await st.llm.ainvoke(prompt)
    text = getattr(resp, "content", None) or str(resp)

    return {
        "answer": text.strip(),
        "docs": [{"content": d.page_content, "meta": d.metadata} for d in docs],
    }
