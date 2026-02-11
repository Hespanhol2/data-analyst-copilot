import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase


def get_database():
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL não encontrada no .env")

    db = SQLDatabase.from_uri(database_url)

    return db

