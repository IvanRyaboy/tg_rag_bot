import sqlalchemy as sa
from .engine import engine

metadata = sa.MetaData()

apartments_ids = sa.Table("apartments_ids", metadata, autoload_with=engine)
apartment = sa.Table("apartments_apartment", metadata, autoload_with=engine)
rent_ids = sa.Table("rent_ids", metadata, autoload_with=engine)
rent = sa.Table("rent_rent", metadata, autoload_with=engine)
