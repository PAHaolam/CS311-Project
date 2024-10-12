from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from .service import ChatbotAssistant
from src.tools.booking import load_booking_tools
import ast
import re
import pandas as pd

router = APIRouter()
assistant = ChatbotAssistant()

# # You can also add more tools for agent to use.
# # This is an example of how you can add tools to the agent and guide you how the agent will route between them.
assistant.add_tools(load_booking_tools())


# --- API Endpoints ---
@router.post("/complete")
async def complete_text(request: Request):
    data = await request.json()
    message = data.get("message")
    response = assistant.complete(message)
    books = []
    match = re.search(r"\{.*?\}", response)
    if match:
        dict_response = ast.literal_eval(match.group())
        response = dict_response["response"]
        ISBNs = dict_response["book_list"]
        if len(ISBNs) > 0:
            df = pd.read_csv("sample_data/sample_data4.csv")
            for ISBN in ISBNs:
                row = df.loc[df['ISBN'] == ISBN]
                if not row.empty:
                    books.append(row.iloc[0].to_dict())
    
    return JSONResponse(content={"response": response, "books": books})
