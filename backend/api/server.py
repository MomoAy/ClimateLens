from core.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    print(conn.execute(text("SELECT version()")).scalar())