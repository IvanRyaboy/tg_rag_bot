import asyncio
import backoff
from typing import Sequence, Dict, Any, List


class VectorStoreService:
    def __init__(self, vs) -> None:
        self._vs = vs

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    async def add_embeddings(
        self,
        texts: Sequence[str],
        embeddings: List[List[float]],
        metadatas: Sequence[Dict[str, Any]] | None,
        ids: Sequence[str] | None,
    ):
        return await asyncio.to_thread(
            self._vs.add_embeddings,
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    async def add_texts(
        self,
        texts: Sequence[str],
        metadatas: Sequence[Dict[str, Any]] | None,
        ids: Sequence[str] | None,
    ):
        return await asyncio.to_thread(
            self._vs.add_texts,
            texts,
            metadatas=metadatas,
            ids=ids,
        )
