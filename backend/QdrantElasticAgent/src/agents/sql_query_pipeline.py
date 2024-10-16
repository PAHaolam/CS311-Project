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
from llama_index.core.llms import ChatResponse
from llama_index.core.schema import NodeWithScore
from llama_index.llms.openai import OpenAI
from typing import List
from decouple import config
from sqlmodel import create_engine, Session, select
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

import itertools
import json
import ast
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.schemas import Book3, BookElasticSearchResponse
from src.embedding.book_elastic_search import ElasticSearch
from src.settings import setting

class SQLQueryPipeline:
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

        self.es = ElasticSearch(
            url=setting.elastic_search_url, index_name=setting.book_elastic_search_index_name
        )

        self.table_infos = [
            {
                "table_name" : "book3",
                "table_summary" : f'''
                This table give information about books in the store.
                It has columns: id, URL, title, gift, description, current_price, original_price, sold, authors, readers, size, num_page, cover_format, weight, book_set, img_url, dop, books_available.

                Some example rows:
                {self.get_db_context(Book3)}
                '''
            }
        ]

        self.sql_database = SQLDatabase(self.engine)
        self.table_node_mapping = SQLTableNodeMapping(self.sql_database)
        self.table_schema_objs = [
            SQLTableSchema(table_name=t["table_name"], context_str=t["table_summary"])
            for t in self.table_infos
        ]  # add a SQLTableSchema for each table

        self.obj_index = ObjectIndex.from_objects(
            self.table_schema_objs,
            self.table_node_mapping,
            VectorStoreIndex,
        )

        self.obj_retriever = self.obj_index.as_retriever(similarity_top_k=3)

        self.sql_retriever = SQLRetriever(self.sql_database)

        self.table_parser_component = FnComponent(fn=self.get_table_context_str)

        self.sql_parser_component = FnComponent(fn=self.parse_response_to_sql)

        self.text2sql_prompt = DEFAULT_TEXT_TO_SQL_PROMPT.partial_format(
            dialect=self.engine.dialect.name
        )

        self.es_mappings = json.dumps(
            self.es.es_client.indices.get_mapping(index=self.es.index_name)[self.es.index_name]['mappings'],
            indent=4
        )

        self.sql2dsl_prompt_str = '''
            Given the mapping: {mappings}
            translate the sql_query: {sql_query}
            in a valid Elasticsearch DSL query
            Note that you only returns the synthesized Elasticsearch DSL query, not any other information such as explaination.
        '''
        self.sql2dsl_prompt_component = FnComponent(fn=self.sql2dsl_prompt)

        self.dsl_parser_component = FnComponent(fn=self.parse_response_to_dsl)

        self.nodes2rows_component = FnComponent(fn=self.nodes_to_rows)

        self.es_retriever_component = FnComponent(fn=self.es_search)

        self.response_synthesis_prompt_str = (
            "Given an input question, synthesize a response from the query results.\n"
            "Query: {query_str}\n"
            "SQL: {sql_query}\n"
            "retrieved rows: {context_str}\n"
            "You will define whether if users are finding some specific books or users dont find the specific books and want to be suggested some books\n"
            "1. if users are finding some specific books and given retrieved rows includes the books, your response should be:\n"
            "Vâng, bên mình có cuốn sách (or truyện depending on Query) ...(Name of books that user expect), bạn có thể tham khảo qua! or Đây là danh sách sách các sách (or truyện depending on Query) liên quan đến ..(Name of books that user expect), mời bạn tham khảo\n"
            "2. if users are finding some specific books and given retrieved rows is empty, your response should be:\n"
            "Xin lỗi, hiện tại bên mình đang không có sách (or truyện depending on Query) ...(Name of books that user expect) mà bạn đang cần, bạn có thể thử tìm sách khác hoặc mình có thể đề xuất cho bạn một số sách\n"
            "3. if users dont find the specific books and want to be suggested some books, your response should be:\n"
            "Đây là một số sách (or truyện depending on Query) mình có thể đề xuất cho bạn\n"
            "Then you can ask the user some other questions that the user might be interested in related to the question.\n"
            "Example:\n"
            "Query: Tôi muốn tìm truyện Doraemon\n"
            "Response: Đây là danh sách truyện Doraemon hiện tại chúng mình đang có, bạn có thể cho mình biết bạn đang muốn tìm tập truyện nào để mình tìm kiếm cho bạn\n"
            "\n"
            "Query: Tôi muốn tìm truyện Naruto"
            "Response: Bên mình truyện Naruto hiện tại đang có rất nhiều, bạn có thể tham khảo qua, đồng thời truyện Naruto bên mình cũng đang ưu đãi giảm giá khá nhiều nhé!"
            "\n"
            "Query: Bạn có thể đề giới thiệu cho tôi một số truyện bạn đang có\n"
            "Response: Đây là một số truyện mình có thể đề xuất cho bạn, nếu bạn quan tâm đến sản phẩm nào có thể cho mình biết nhé!\n"
            "\n"
            "Response: "
        )
        self.response_synthesis_prompt = PromptTemplate(
            self.response_synthesis_prompt_str,
        )
        self.response_and_node_component = FnComponent(fn=self.return_response_and_node)

        self.llm = OpenAI(model="gpt-3.5-turbo")

        self.qp = QP(
            modules={
                "input": InputComponent(),
                "table_retriever": self.obj_retriever,
                "table_output_parser": self.table_parser_component,
                "text2sql_prompt": self.text2sql_prompt,
                "text2sql_llm": self.llm,
                "sql_output_parser": self.sql_parser_component,
                "sql2dsl_prompt": self.sql2dsl_prompt_component,
                "sql2dsl_llm": self.llm,
                "dsl_output_parser": self.dsl_parser_component,
                "sql_retriever": self.sql_retriever,
                "nodes_to_rows": self.nodes2rows_component,
                "es_retriever": self.es_retriever_component,
                "response_synthesis_prompt": self.response_synthesis_prompt,
                "response_synthesis_llm": self.llm,
                "return_response_and_node": self.response_and_node_component,
            },
            verbose=True,
        )
        self.create_links()
        

    def get_db_context(self, table, size: int = 5):
        result = []
        with Session(self.engine) as session:
            stmt = select(table).limit(size)
            data = session.exec(stmt)
            for row in data:
                result.append(row)

        table_columns = table.__table__.columns.keys()
        context_str = " | ".join(table_columns)
        # Make a context str for llm to understand
        for row in result:
            context_str += "\n"
            context_str += " | ".join([str(getattr(row, col)) for col in table_columns])

        return context_str


    def get_table_context_str(self, table_schema_objs: List[SQLTableSchema]):
        """Get table context string."""
        context_strs = []
        for table_schema_obj in table_schema_objs:
            table_info = self.sql_database.get_single_table_info(
                table_schema_obj.table_name
            )
            if table_schema_obj.context_str:
                table_opt_context = " The table description is: "
                table_opt_context += table_schema_obj.context_str
                table_info += table_opt_context

            context_strs.append(table_info)
        return "\n\n".join(context_strs)


    def adjust_sql_query(self, sql_query):
        # Find the position of 'SELECT' and 'FROM'
        select_index = sql_query.upper().find("SELECT")
        from_index = sql_query.upper().find("FROM")

        # Check if both 'SELECT' and 'FROM' are present in the query
        if select_index == -1 or from_index == -1:
            return sql_query  # Return the original query if it's invalid

        # Replace the column names between SELECT and FROM with '*'
        adjusted_query = sql_query[:select_index + len("SELECT")] + " title, URL, current_price, original_price, img_url " + sql_query[from_index:]
        
        return adjusted_query
    

    def parse_response_to_sql(self, response: ChatResponse) -> str:
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
        response = response.strip().strip("```").strip()
        response = self.adjust_sql_query(response)
        return response 


    def sql2dsl_prompt(self, sql_query: str) -> str:
        prompt = self.sql2dsl_prompt_str.format(mappings = self.es_mappings,
                                                sql_query = sql_query)
        return prompt
    

    def parse_response_to_dsl(self, response: ChatResponse) -> str:
        """Parse response to SQL."""
        response = response.message.content
        return response

    
    def extract_columns(self, sql_query):
        # Parse the SQL query
        parsed = sqlparse.parse(sql_query)
        statement = parsed[0]  # Chỉ lấy câu truy vấn đầu tiên nếu có nhiều câu

        # Tìm các phần SELECT trong câu truy vấn
        select_seen = False
        columns = []
        
        for token in statement.tokens:
            # Kiểm tra nếu từ khóa là SELECT
            if select_seen:
                # Nếu gặp dấu phẩy hoặc danh sách các cột
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        columns.append(str(identifier))
                elif isinstance(token, Identifier):
                    columns.append(str(token))
                elif token.ttype is Keyword:
                    # Dừng khi gặp từ khóa khác (ví dụ: FROM)
                    break
            elif token.ttype is DML and token.value.upper() == 'SELECT':
                select_seen = True
        
        return columns
    

    def nodes_to_rows(self, sql_retriever: List[NodeWithScore], es_retriever: list[BookElasticSearchResponse]):
        rows = [node.node.metadata['result'] for node in sql_retriever]
        rows = list(itertools.chain(*rows))
        rows = [{"title": row[0],
                 "URL": row[1],
                 "current_price": row[2],
                 "original_price": row[3],
                 "img_url": row[4],} for row in rows[:24]]
        if len(rows)>0:
            return str(rows)
        
        rows2 = [{"URL": node.URL,
                  "title": node.title,
                  "current_price": node.current_price,
                  "original_price": node.original_price,
                  "img_url": node.img_url} 
                  for node in es_retriever[:24]]
        return str(rows2)
    

    def es_search(self, dsl_query):
       search_body = ast.literal_eval(dsl_query)
       es_retriever = self.es.search(search_body)
       return es_retriever
    

    def return_response_and_node(self, rows, sql_query: str, response: ChatResponse):
        response_dict = {"rows": eval(rows), "sql_query": sql_query, "response": response.message.content}
        response_json = json.dumps(response_dict, ensure_ascii=False)
        return response_json
    
    def create_links(self):
        self.qp.add_chain(["input", "table_retriever", "table_output_parser"])
        self.qp.add_link("input", "text2sql_prompt", dest_key="query_str")
        self.qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
        self.qp.add_chain(
            ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
        )
        self.qp.add_chain(
            ["sql_output_parser", "sql2dsl_prompt", "sql2dsl_llm", "dsl_output_parser", "es_retriever"]
        )
        self.qp.add_link(
            "sql_retriever", "nodes_to_rows", dest_key="sql_retriever"
        )
        self.qp.add_link(
            "es_retriever", "nodes_to_rows", dest_key="es_retriever"
        )
        self.qp.add_link(
            "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
        )
        self.qp.add_link(
            "nodes_to_rows", "response_synthesis_prompt", dest_key="context_str"
        )
        self.qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
        self.qp.add_link("response_synthesis_prompt", "response_synthesis_llm")
        self.qp.add_link(
            "response_synthesis_llm", "return_response_and_node", dest_key="response"
        )
        self.qp.add_link(
            "sql_output_parser", "return_response_and_node", dest_key="sql_query"
        )
        self.qp.add_link(
            "nodes_to_rows", "return_response_and_node", dest_key="rows"
        )

    def answer(self, query_str):
        response = self.qp.run(
            query = query_str
        )
        return response#json.dumps(response, ensure_ascii=False)