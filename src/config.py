import os
import dotenv

dotenv.load_dotenv()
SQL_USER = os.environ["SQL_USER"]
SQL_PASSWORD = os.environ["SQL_PASSWORD"]
SQL_HOST = os.environ["SQL_HOST"]
SQL_DB=os.environ["SQL_DB"]
SQL_PORT=os.environ["SQL_PORT"]
SQL_URL = f"postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB}"
TIME_ZONE=os.environ["TIME_ZONE"]
WEB_PORT=int(os.environ["WEB_PORT"])