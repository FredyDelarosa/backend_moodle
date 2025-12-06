from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import settings

DATABASE_URL = f"mysql+aiomysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL.replace("+aiomysql", "+pymysql"), future=True)
metadata = MetaData()
