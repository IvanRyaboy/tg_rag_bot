from typing import Sequence, Mapping, Any, List
from content import apartment_content, apartment_metadata, rent_content, rent_metadata
from utils.embedding_service import EmbeddingService
from utils.vector_store_service import VectorStoreService


async def process_apartment_chunk(
    rows: Sequence[Mapping[str, Any]],
    emb_svc: EmbeddingService,
    vs_svc: VectorStoreService,
):
    ids: List[str] = []
    texts: List[str] = []
    metadatas: List[dict] = []

    for row in rows:
        ids.append(row["id"])
        texts.append(apartment_content(row))
        metadatas.append(apartment_metadata(row))

    vectors = await emb_svc.embed_batch(texts)

    try:
        await vs_svc.add_embeddings(texts=texts, embeddings=vectors, metadatas=metadatas, ids=ids)
    except AttributeError:
        await vs_svc.add_texts(texts=texts, metadatas=metadatas, ids=ids)


async def process_rent_chunk(
    rows: Sequence[Mapping[str, Any]],
    emb_svc: EmbeddingService,
    vs_svc: VectorStoreService,
):
    ids: List[str] = []
    texts: List[str] = []
    metadatas: List[dict] = []

    for row in rows:
        ids.append(row["id"])
        texts.append(rent_content(row))
        metadatas.append(rent_metadata(row))

    vectors = await emb_svc.embed_batch(texts)

    try:
        await vs_svc.add_embeddings(texts=texts, embeddings=vectors, metadatas=metadatas, ids=ids)
    except AttributeError:
        await vs_svc.add_texts(texts=texts, metadatas=metadatas, ids=ids)
