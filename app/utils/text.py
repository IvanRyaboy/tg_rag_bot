from typing import List


def chunk_text(s: str, limit: int = 4096) -> List[str]:
    """
    Чанкует текст для передачи в llm.
    :param s:
    :param limit:
    :return: List[str]
    """
    if len(s) <= limit:
        return [s]
    parts, start = [], 0
    while start < len(s):
        end = min(len(s), start + limit)
        nl = s.rfind("\n", start, end)
        if nl != -1 and nl > start + limit // 2:
            end = nl + 1
        parts.append(s[start:end])
        start = end
    return parts
