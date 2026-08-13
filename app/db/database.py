import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_database = os.getenv("DB_DATABASE")

engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_password}@{db_host}/{db_database}"
)
