# Goal: Provide db connection to all modules
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_name = os.environ["POSTGRES_DB"]
db_username = os.environ["POSTGRES_USER"]
db_password = os.environ["POSTGRES_PASSWORD"]

DB_URL = URL.create(
    "postgresql+psycopg",
    username=db_username,
    password=db_password,
    host=db_host,
    database=db_name,
    port=int(db_port)
    )

engine = create_engine(DB_URL)

local_session = sessionmaker(bind=engine)

