from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from .service import ChatbotAssistant
from src.constants import FORMATTING_PROMPT
import ast
import re
import pandas as pd
from decouple import config
from sqlmodel import create_engine, Session
from sqlalchemy import text
from icecream import ic


router = APIRouter()
assistant = ChatbotAssistant()

SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# # You can also add more tools for agent to use.
# # This is an example of how you can add tools to the agent and guide you how the agent will route between them.
#assistant.add_tools(load_booking_tools())


# --- API Endpoints ---
@router.post("/complete")
async def complete_text(request: Request):
    data = await request.json()
    message = data.get("message")
    response = assistant.complete(message)
    books = []

    try:
        dict_response = ast.literal_eval(response)
        response = dict_response["response"]
        rows = dict_response["rows"]
        
        for row in rows:
            book = {
                "title": row['title'],
                "URL": row["URL"],
                "current_price": row["current_price"],
                "original_price": row["original_price"],
                "img_url": row["img_url"],
                "type": row["type"],
            }
            books.append(book)

        chat_store_key = assistant.query_engine.memory.chat_store_key
        chat_store = assistant.query_engine.memory.chat_store.store
        try:
            chat_store[chat_store_key].pop(-3)
            chat_store[chat_store_key].pop(-2)
            chat_store[chat_store_key].pop(-1)
            chat_store.setdefault(chat_store_key, []).append(ChatMessage(content=response, role=MessageRole.ASSISTANT))
            print("Modify chat store successfully!")
        except Exception as e:
            print(f"Modify chat store unsuccessfully! Error: {e}")

    except SyntaxError:
        pass
    
    return JSONResponse(content={"response": response, "books": books})


@router.post("/init_books")
async def init_books():
    books = []
    with Session(engine) as session:
        # Execute the query
        newest_result = session.exec(text("SELECT title, URL, current_price, original_price, img_url FROM book3 ORDER BY dop DESC LIMIT 12;"))
        trending_result = session.exec(text("SELECT title, URL, current_price, original_price, img_url FROM book3 ORDER BY sold DESC LIMIT 12;"))
        
        # Fetch all rows from the result
        newest_rows = newest_result.fetchall()
        trending_rows = trending_result.fetchall()
        
    for row in newest_rows:
        book = {
            "title": row[0],
            "URL": row[1],
            "current_price": row[2],
            "original_price": row[3],
            "img_url": row[4],
            "type": "Mới nhất",
        }
        books.append(book)

    for row in trending_rows:
        book = {
            "title": row[0],
            "URL": row[1],
            "current_price": row[2],
            "original_price": row[3],
            "img_url": row[4],
            "type": "Bán chạy nhất",
        }
        books.append(book)

    return JSONResponse(content={"books": books})
