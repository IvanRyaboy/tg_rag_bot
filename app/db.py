from contextlib import contextmanager
from typing import Iterable, Sequence, Mapping, Any

import psycopg
from psycopg.rows import dict_row

from settings import settings
from sql import SQL_APARTMENTS, SQL_RENT

BATCH_SIZE = 256


def _to_psycopg_dsn(uri: str) -> str:
    return uri.replace("postgresql+psycopg://", "postgresql://", 1)


@contextmanager
def pg_connection():
    if not settings.PGVECTOR_CONN:
        raise RuntimeError("PGVECTOR_CONN обязателен")
    dsn = _to_psycopg_dsn(settings.PGVECTOR_CONN)
    with psycopg.connect(dsn, autocommit=False) as conn:
        yield conn


def stream_apartments_rows_by_ids(conn, ids, batch_size: int):
    for i in range(0, len(ids), batch_size):
        chunk_ids = ids[i:i+batch_size]
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(SQL_APARTMENTS, (chunk_ids,))
            yield cur.fetchall()


def stream_rent_rows_by_ids(conn, ids, batch_size: int):
    for i in range(0, len(ids), batch_size):
        chunk_ids = ids[i:i+batch_size]
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(SQL_RENT, (chunk_ids,))
            yield cur.fetchall()
