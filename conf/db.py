import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

URI = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

# engine = create_engine(URI, echo=True, pull_size=5, max_overflow=0)
engine = create_engine(URI)
SessionLocal = sessionmaker(bind=engine)
