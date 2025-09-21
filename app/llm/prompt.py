from typing import List
from langchain.schema import Document


def build_prompt(query: str, docs: List[Document]) -> str:
    context = "\n\n".join(
        f"Listing {i+1} | id={d.metadata.get('apartment_id')}:\n"
        f"{d.page_content}\n"
        f"Metadata: {d.metadata}"
        for i, d in enumerate(docs)
    ) or "контекст не предоставлен"

    return f"""
Ты — виртуальный риэлтор и технический консультант по недвижимости.
Отвечай кратко, точно и опирайся исключительно на предоставленный контекст.

Контекст:
{context}

Правила:
- Используй только факты из контекста (page_content + metadata).
- Если информации недостаточно — задай уточняющий вопрос.
- Будь лаконичен и структурирован.
- Рассчитай price_per_m2 = round(price / total_area), если есть оба поля.
- Указывай geo (lat/lon) и link, если они есть в metadata.
- Отмечай область знаний: недвижимость. Оцени сложность: базовая/средняя/продвинутая.

Вопрос пользователя: {query}

Ответ:
""".strip()
