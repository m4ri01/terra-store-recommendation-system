from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import MetaData

metadata = MetaData()

master_user = Table(
    "master_user",
    metadata,
    Column("id", GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL),
    Column("name", String(255), nullable=False),
    Column("address", String(255), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
)