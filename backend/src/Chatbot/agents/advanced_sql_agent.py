import sys
import enum
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from llama_index.core.objects import SQLTableSchema, SQLTableNodeMapping, ObjectIndex
from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_TO_SQL_PROMPT
from llama_index.core.query_pipeline import (
    Link,
    FnComponent,
    InputComponent,
    QueryPipeline as QP,
    CustomQueryComponent,
)
from llama_index.core.retrievers import SQLRetriever
from llama_index.core import SQLDatabase, VectorStoreIndex, PromptTemplate
from llama_index.core import Settings as llamaSettings
from llama_index.llms.groq import Groq
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.llms import ChatResponse
from llama_index.core.schema import NodeWithScore
from typing import List
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

# 1. Define object 
prompt = (
    "This table give information about books in the store.\n"
    "It has columns: id, url, title, description, current_price, original_price, sold, authors, age_reader, gift, width, height, num_page, format, weight.\n"
    "\n"
    "Some example rows:\n"
    f"{get_db_context()}"
)

sql_database = SQLDatabase(engine)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    SQLTableSchema(table_name="book", context_str=prompt)
]  # add a SQLTableSchema for each table

obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
obj_retriever = obj_index.as_retriever(similarity_top_k=3)

sql_retriever = SQLRetriever(sql_database)


# 2.
def get_table_context_str(table_schema_objs: List[SQLTableSchema]):
    """Get table context string."""
    context_strs = []
    for table_schema_obj in table_schema_objs:
        table_info = sql_database.get_single_table_info(
            table_schema_obj.table_name
        )
        if table_schema_obj.context_str:
            table_opt_context = " The table description is: "
            table_opt_context += table_schema_obj.context_str
            table_info += table_opt_context

        context_strs.append(table_info)
    return "\n\n".join(context_strs)


table_parser_component = FnComponent(fn=get_table_context_str)


def parse_response_to_sql(response: ChatResponse) -> str:
    """Parse response to SQL."""
    response = response.message.content
    sql_query_start = response.find("SQLQuery:")
    if sql_query_start != -1:
        response = response[sql_query_start:]
        if response.startswith("SQLQuery:"):
            response = response[len("SQLQuery:") :]
    sql_result_start = response.find("SQLResult:")
    if sql_result_start != -1:
        response = response[:sql_result_start]
    return response.strip().strip("```").strip()


sql_parser_component = FnComponent(fn=parse_response_to_sql)

text2sql_prompt = DEFAULT_TEXT_TO_SQL_PROMPT.partial_format(
    dialect=engine.dialect.name
)

response_synthesis_prompt_str = (
    "Given an input question, synthesize a response from the query results.\n"
    "Query: {query_str}\n"
    "SQL: {sql_query}\n"
    "SQL Response: {context_str}\n"
    "Response: "
)
response_synthesis_prompt = PromptTemplate(
    response_synthesis_prompt_str,
)

def return_response_and_node(response: ChatResponse, retriever: List[NodeWithScore]):
    return {"response": response, "nodes": retriever}

response_and_node_component = FnComponent(fn=return_response_and_node)

llm = Groq(model="llama3-8b-8192", api_key=config("GROQ_API_KEY"))

qp = QP(
    modules={
        "input": InputComponent(),
        "table_retriever": obj_retriever,
        "table_output_parser": table_parser_component,
        "text2sql_prompt": text2sql_prompt,
        "text2sql_llm": llm,
        "sql_output_parser": sql_parser_component,
        "sql_retriever": sql_retriever,
        "response_synthesis_prompt": response_synthesis_prompt,
        "response_synthesis_llm": llm,
        "return_response_and_node": response_and_node_component,
    },
    verbose=True,
)

qp.add_chain(["input", "table_retriever", "table_output_parser"])
qp.add_link("input", "text2sql_prompt", dest_key="query_str")
qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
qp.add_chain(
    ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
)
qp.add_link(
    "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
)
qp.add_link(
    "sql_retriever", "response_synthesis_prompt", dest_key="context_str"
)
qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
qp.add_link("response_synthesis_prompt", "response_synthesis_llm")
qp.add_link("sql_retriever", "return_response_and_node", dest_key="retriever")
qp.add_link("response_synthesis_llm", "return_response_and_node", dest_key="response")