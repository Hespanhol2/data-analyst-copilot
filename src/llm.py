import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def get_llm():
    load_dotenv()

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
