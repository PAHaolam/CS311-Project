from fastapi import FastAPI
from fastapi.responses import JSONResponse
#from src.simple_chatbot import ask_question
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.Chatbot.agents import qp
#from src.Chatbot.settings import setting

class Message(BaseModel):
    message: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


#agent = SQLAgent(setting=setting)


@app.post("/chat")
def chat(message: Message):
    message = message.message
    response = qp.run(
        query = message
    )

    answer = response['response'].message.content

    title_books = []
    for node in response['nodes']:
        metadata = node.node.metadata
        if 'title' in metadata['col_keys']:
            title_idx = metadata['col_keys'].index('title')
            for result in metadata['result']:
                title_books.append(result[title_idx])
    #response = agent.query(message.message)
    #response = "Chatbot đang không hoạt động, bạn vui lòng trở lại sau nhé, xin cảm ơn!"
    response_content = {
        "question": message,
        "answer": answer,
        "title_books": title_books,
    }
    return JSONResponse(content=response_content, status_code=200)
