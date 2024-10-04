import sys
import enum
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from llama_index.core.objects import SQLTableSchema, SQLTableNodeMapping, ObjectIndex
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core import Settings as llamaSettings
from llama_index.core.bridge.pydantic import BaseModel
from llama_index.llms.groq import Groq
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from decouple import config
from Chatbot.database.run import get_db_context, engine
from Chatbot.prompt import REFINE_PROMPT, RESTRICT_PROMPT
from Chatbot.settings import MessageRole, Settings


llamaSettings.embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="my-custom-embedding",             #Lấy tên của embedding model gán vào biến deployment_name
    api_key=config("AZURE_OPENAI_API_KEY"),            #Lấy azure openai api key gán vào biến api_key
    azure_endpoint=config("AZURE_OPENAI_ENDPOINT"),    #lấy azure openao endpoint gán vào biến azure_endpoint
    api_version="2024-05-01-preview",
)


class Message(BaseModel):
    role: str
    content: str


class SQLAgent:
    def __init__(self, setting: Settings):
        prompt = (
            "This table give information about books in the store.\n"
            "It has columns: id, url, title, description, current_price, original_price, sold, authors, age_reader, gift, width, height, num_page, format, weight.\n"
            "\n"
            "Some example rows:\n"
            f"{get_db_context()}"
        )

        self.setting = setting

        self.sql_database = SQLDatabase(engine, include_tables=["book"])
        self.table_node_mapping = SQLTableNodeMapping(self.sql_database)
        self.table_schema_objs = [
            (SQLTableSchema(table_name="book", context_str=prompt))
        ]
        self.obj_index = ObjectIndex.from_objects(
            self.table_schema_objs,
            self.table_node_mapping,
            VectorStoreIndex,
        )

        self.history: list[Message] = []

        self.system_prompt = """The unit of sold is copy, the unit of width and height is centimeter, the unit of weight is gram."""

        llm = self.load_model(
            self.setting.type, self.setting.llm, self.system_prompt.strip("\n")
        )

        self.refine_llm = self.load_model(
            self.setting.type,
            self.setting.llm,
            REFINE_PROMPT.format(num=setting.number_of_msgs),
        )

        self.query_engine = SQLTableRetrieverQueryEngine(
            self.sql_database,
            self.obj_index.as_retriever(similarity_top_k=3),
            llm=llm,
            streaming=True,
        )

    def add_message(self, role: str, content: str):
        if role == MessageRole.system:  # noqa
            return
        self.history.append(Message(role=role, content=content))

    def get_history(self, num_history: int):
        history = self.history[-num_history:]
        return "\n".join([f"- {msg.role}: {msg.content}" for msg in history])

    def load_model(
        self, model_type: str, model_name: str, system: str = ""
    ) -> FunctionCallingLLM:
        if model_type == "groq":
            return Groq(model=model_name, api_key=config("GROQ_API_KEY"), system_prompt=system)
        else:
            raise ValueError("Model type not supported")

    def refine_question(self, question: str):
        prompt = f"History: {self.get_history(self.setting.number_of_msgs)}\nQuestion: {question}\nYour refined question: "
        response = self.refine_llm.complete(prompt)
        return response.text# + RESTRICT_PROMPT

    def query(self, question: str) -> str:
        prompt = self.refine_question(question)
        response = self.query_engine.query(prompt)
        print("SQLAgent answer:")
        return response