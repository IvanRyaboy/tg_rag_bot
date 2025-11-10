import sqlalchemy as sa
from app.database.engine import session_scope
from app.database.tables import apartments_ids, rent_ids
import uuid


def get_unembedded_apartments_ids(old_status: str = "READY", new_status: str = "PROCESSED") -> list[uuid]:
    stmt = (
        sa.update(apartments_ids)
        .where(apartments_ids.c.status == sa.bindparam("old"))
        .values(status=sa.bindparam("new"))
        .returning(apartments_ids.c.apartment_id)
    )
    with session_scope() as s:
        ids = [r[0] for r in s.execute(stmt, {"old": old_status, "new": new_status})]
        return ids


def get_unembedded_rent_ids(old_status: str = "READY", new_status: str = "PROCESSED") -> list[uuid]:
    stmt = (
        sa.update(rent_ids)
        .where(rent_ids.c.status == sa.bindparam("old"))
        .values(status=sa.bindparam("new"))
        .returning(rent_ids.c.rent_id)
    )
    with session_scope() as s:
        ids = [r[0] for r in s.execute(stmt, {"old": old_status, "new": new_status})]
        return ids

#
# if __name__ == "__main__":
#     print(get_unembedded_ids())
