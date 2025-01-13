import sys
import json
import pandas as pd
from thefuzz import process
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain_core.tools import Tool

#from src.agents.sql_query_pipeline import SQLQueryPipeline

file_path = r'D:\HK5\AIEngineer\CS311_Project\backend\RAG_tool\data\sample_data5.csv' 
df_product = pd.read_csv(file_path)

def load_product_search_tool():
    # qp = SQLQueryPipeline()
    def answer_query(query_str: str) -> str:
        """
        A helpfull function to answer a book query.

        Args:
            query_str (str): The query string to search for.

        Returns:
            str: The answer to the query.
        """
        query_str = query_str.lower().replace("truyện", "").strip()
        product_list = df_product['title'].tolist()
        list_product_name_by_fuzzy = process.extract(query_str, product_list, limit=5)

        result_str = f"Một số sản phẩm liên quan đến {query_str} gồm: \n"
        for index, product_name_by_fuzzy in enumerate(list_product_name_by_fuzzy):
            product_name_by_fuzzy = product_name_by_fuzzy[0]
            product_info = df_product[df_product['title'] == product_name_by_fuzzy]
            if not product_info.empty:
                name = product_info.iloc[0]['title']
                price = product_info.iloc[0]['currentPrice']
                # description = product_info.iloc[0]['description']
                url = product_info.iloc[0]['URL']
                result_str += f"{index+1}- Sản phẩm: {name}, Giá: {price}, Link sản phẩm: {url} \n"
        
        return result_str
        

    return Tool(
        name="Product Search tool",
        func=answer_query,
        description="""
            Trả lời những câu hỏi liên quan đến tìm kiếm thông tin về một sản phẩm cụ thể của công công ty.
            Những loại câu hỏi không liên quan đến tìm kiếm sản phẩm cụ thể như:
            - Sản phẩm bên em có gì
            - A xin thông tin sản phẩm bên em
            - Danh mục sản phẩm bên em có gì
            - Bên em bán những gì
            - Bên em có những loại sản phẩm nào
            - Bên em bán những sản phẩm gì
            - Em có sp gì
            - sp bên em gồm những gì
        """
    )
