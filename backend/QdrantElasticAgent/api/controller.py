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

router = APIRouter()
assistant = ChatbotAssistant()

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
    match = re.search(r"\{.*?\}", response)
    # match2 = re.findall(r'[A-Z0-9]{10}', response)
    if match:
        dict_response = ast.literal_eval(match.group())
        response = dict_response["response"]
        rows = dict_response["rows"]

        for row in rows:
            book = {
                "title": row[0],
                "URL": row[1],
                "current_price": row[2],
                "original_price": row[3],
                "img_url": row[4]
            }
            books.append(book)

    # elif match2:
    #     response = OpenAI().complete(FORMATTING_PROMPT.format(
    #         response = response
    #     ))
    #     match = re.search(r"\{.*?\}", str(response))
    #     if match:
    #         dict_response = ast.literal_eval(match.group())
    #         response = dict_response["response"]
    #         ISBNs = dict_response["book_list"]

    #         chat_store_key = assistant.query_engine.memory.chat_store_key
    #         chat_store = assistant.query_engine.memory.chat_store.store
    #         try:
    #             chat_store[chat_store_key].pop(-1)
    #             chat_store.setdefault(chat_store_key, []).append(ChatMessage(content=match.group(), role=MessageRole.ASSISTANT))
    #             print("Modify chat store successfully!")
    #         except Exception as e:
    #             print(f"Modify chat store unsuccessfully! Error: {e}")

    #         if len(ISBNs) > 0:
    #             df = pd.read_csv("sample_data/sample_data4.csv")
    #             for ISBN in ISBNs:
    #                 row = df.loc[df['ISBN'] == ISBN]
    #                 if not row.empty:
    #                     books.append(row.iloc[0].to_dict())
    
    return JSONResponse(content={"response": response, "books": books})
