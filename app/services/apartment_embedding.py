import asyncio
from app.context_managers import embed_context
from app.db import pg_connection, stream_apartments_rows_by_ids
from app.utils.embedding_service import EmbeddingService
from app.utils.vector_store_service import VectorStoreService
from app.pipeline import process_apartment_chunk
from app.utils.update_ids import get_unembedded_apartments_ids

BATCH_SIZE = 256


async def apartment_embedding():
    ids = get_unembedded_apartments_ids()
    if not ids:
        print("No new apartments for embedding")
        return

    async with embed_context("apartments") as r:
        emb_svc = EmbeddingService(r.emb)
        vs_svc = VectorStoreService(r.vs)

        with pg_connection() as conn:
            for rows in stream_apartments_rows_by_ids(conn, ids, BATCH_SIZE):
                await process_apartment_chunk(rows, emb_svc, vs_svc)

