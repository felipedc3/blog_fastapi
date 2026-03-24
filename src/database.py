import os

import sqlalchemy
import databases


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

if DATABASE_URL.startswith("sqlite"):
    engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
else:
    engine = sqlalchemy.create_engine(DATABASE_URL)