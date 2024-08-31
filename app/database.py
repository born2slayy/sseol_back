from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("DB_USER")    
passwd = os.getenv("DB_PASSWD")
host = os.getenv("DB_HOST")     
port = os.getenv("DB_PORT")     
db = os.getenv("DB_NAME")      

DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

print(port)

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
