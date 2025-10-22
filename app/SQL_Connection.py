from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

print(os.getenv("DATABASE_USER"))

DataBase_User = os.getenv("DATABASE_USER")
DataBase_Pass = quote_plus(os.getenv("DATABASE_PASS"))
DataBase_Host = os.getenv("DATABASE_HOST", "localhost")
DataBase_Name = os.getenv("DATABASE_NAME", "notes_db")



Connection_URL = f"mysql+pymysql://{DataBase_User}:{DataBase_Pass}@{DataBase_Host}/{DataBase_Name}"

engine = create_engine(Connection_URL)
SessionMaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()
