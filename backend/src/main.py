from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.chatbot import ask_question
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Message(BaseModel):
    message: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

@app.post("/chat")
def chat(message: Message):
    response = ask_question(message.message)
    #response = "Chatbot đang không hoạt động, bạn vui lòng trở lại sau nhé, xin cảm ơn!"
    response_content = {
        "question": message.message,
        "answer": response
    }
    return JSONResponse(content=response_content, status_code=200)
