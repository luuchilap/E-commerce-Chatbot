from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic
from loguru import logger

from utils import chat_with_llm, init_conversation

app = FastAPI()
security = HTTPBasic()

qa = init_conversation("data/products_fpt.csv")

@app.post("/")
def query(text: str):
    logger.info(f"User: {text}")
    response = chat_with_llm(qa, text)
    return {"response": response}

