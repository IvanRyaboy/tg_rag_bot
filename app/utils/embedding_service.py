import backoff
from typing import Sequence, List


class EmbeddingService:
    def __init__(self, emb) -> None:
        self._emb = emb

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    async def embed_batch(self, texts: Sequence[str]) -> List[List[float]]:
        if not texts:
            return []
        return await self._emb.aembed_documents(list(texts))
