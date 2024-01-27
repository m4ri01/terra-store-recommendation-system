import pandas as pd
import dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()
SQL_USER = os.environ["SQL_USER"]
SQL_PASSWORD = os.environ["SQL_PASSWORD"]
SQL_HOST = os.environ["SQL_HOST_LOCAL"]
SQL_DB=os.environ["SQL_DB"]
SQL_PORT=os.environ["SQL_PORT"]
SQL_URL = f"postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB}"

engine = create_engine(SQL_URL)
Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.master_user
Product = Base.classes.master_product
Interactions = Base.classes.user_interactions
Purchase = Base.classes.user_purchase

Session = sessionmaker(bind=engine)
session = Session()


interactions = pd.read_csv("data/new_interactions.csv")
product = pd.read_csv("data/new_product.csv")
purchase = pd.read_csv("data/new_purchase.csv")

purchase_user_id = purchase["customer_id"].values
purchase_product_id = purchase["product_id"].values

customer_id_uuid = []
product_id_uuid = []

for c,p in zip(purchase_user_id,purchase_product_id):
    customer_uuid = interactions[interactions["customer_id"]==c]["uuid"].values[0]
    product_uuid = product[product["product_id"]==p]["uuid"].values[0]
    customer_id_uuid.append(customer_uuid)
    product_id_uuid.append(product_uuid)

purchase["customer_uuid"] = customer_id_uuid
purchase["product_uuid"] = product_id_uuid

print("Seed Product Data..")
for idx,row in product.iterrows():
    new_product = Product(
        id=row["uuid"],
        product_name=row["product_name"],
        category=row["category"],
        price=row["price"],
        ratings=row["ratings"]
    )
    session.add(new_product)
session.commit()

print("Seed Interactions Data..")
for idx,row in interactions.iterrows():
    new_user = User(
        id=row["uuid"],
        name=row["name"],
        address=row["address"],
    )
    session.add(new_user)
session.commit()

print("Seed interactions Data..")
for idx,row in interactions.iterrows():
    new_interactions = Interactions(
        user_id=row["uuid"],
        time_spent=row["time_spent"],
        page_views=row["page_views"],
    )
    session.add(new_interactions)
session.commit()

print("Seed purchase Data..")
for idx,row in purchase.iterrows():
    new_purchase = Purchase(
        user_id=row["customer_uuid"],
        product_id=row["product_uuid"],
        ratings=row["user_ratings"],
    )
    session.add(new_purchase)
session.commit()

session.close()
print("Finish Seed Data..")