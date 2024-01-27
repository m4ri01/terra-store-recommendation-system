from sqlalchemy import Table, Column, String, DateTime, Integer, Float
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import MetaData

metadata = MetaData()

master_product = Table(
    "master_product",
    metadata,
    Column("id", GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL),
    Column("product_name", String(255), nullable=False),
    Column("category", String(255), nullable=False),
    Column("price", Integer, nullable=False),
    Column("ratings", Float, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
)