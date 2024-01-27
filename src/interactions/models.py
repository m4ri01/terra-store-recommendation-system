from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import MetaData
from src.user.models import master_user

metadata = MetaData()

user_interactions = Table(
    "user_interactions",
    metadata,
    Column("id", GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL),
    Column("user_id",GUID,ForeignKey(master_user.c.id),nullable=False),
    Column("time_spent",Integer,nullable=False),
    Column("page_views",Integer,nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

)