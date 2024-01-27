from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import MetaData
from src.user.models import master_user
from src.product.models import master_product

metadata = MetaData()
user_purchase = Table(
    "user_purchase",
    metadata,
    Column("id", GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL),
    Column("user_id",GUID,ForeignKey(master_user.c.id),nullable=False),
    Column("product_id",GUID,ForeignKey(master_product.c.id),nullable=False),
    Column("ratings",Float,nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
)