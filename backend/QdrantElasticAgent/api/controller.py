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
                "img_url": row["img_url"]
            }
            books.append(book)
    except SyntaxError:
        pass
    
    return JSONResponse(content={"response": response, "books": books})
