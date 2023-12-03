from sqlmodel import create_engine
from core.keys.secrets import DATABASE_URL


db_engine = create_engine(DATABASE_URL)
