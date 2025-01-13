from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from .service import ChatbotAssistant
from dotenv import load_dotenv

load_dotenv(override=True)


router = APIRouter()
assistant = ChatbotAssistant()

file_path = r'D:\HK5\AIEngineer\CS311_Project\backend\RAG_tool\data\sample_data5.csv' 
df_product = pd.read_csv(file_path)

# --- API Endpoints ---
@router.post("/complete")
async def complete_text(request: Request):
    data = await request.json()
    message = data.get("message")
    response = assistant.complete(message)
    
    return JSONResponse(content={"response": response})


@router.post("/init_books")
async def init_books():
    books = []

    df_sorted = df_product.sort_values(by='dateOfPublication', ascending=False)
    newest_rows = df_sorted[['title', 'URL', 'currentPrice', 'originalPrice', 'imgURL']].head(12)

    df_sorted = df_product.sort_values(by='sold', ascending=False)
    trending_rows = df_sorted[['title', 'URL', 'currentPrice', 'originalPrice', 'imgURL']].head(12)

    for row in newest_rows.iterrows():
        book = {
            "title": row[1]['title'],
            "URL": row[1]['URL'],
            "current_price": row[1]['currentPrice'],
            "original_price": row[1]['originalPrice'],
            "img_url": row[1]['imgURL'],
            "type": "Mới nhất",
        }
        books.append(book)

    for row in trending_rows.iterrows():
        book = {
            "title": row[1]['title'],
            "URL": row[1]['URL'],
            "current_price": row[1]['currentPrice'],
            "original_price": row[1]['originalPrice'],
            "img_url": row[1]['imgURL'],
            "type": "Bán chạy nhất",
        }
        books.append(book)

    return JSONResponse(content={"books": books})
