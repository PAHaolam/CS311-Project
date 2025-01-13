from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from RAG_tool.api.controller import router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"]
)

app.include_router(router, prefix="/v1")
