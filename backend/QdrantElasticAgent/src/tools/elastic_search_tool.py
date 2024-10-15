import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.settings import setting
from src.schemas import Book3
from src.embedding.book_elastic_search import ElasticSearch
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool

def load_elastic_search_tool():
    es = ElasticSearch(
        url=setting.elastic_search_url, index_name=setting.book_elastic_search_index_name
    )

    llm = OpenAI(model=setting.model)

    RESPONSE_SYNTHESIS_PROMPT = '''
    Given an input question from user, synthesize a response from the list of retrieved rows.
    Query: {query_str}
    retrieved rows: {retrieved_rows}
    You will define whether if users are finding some specific books or users dont find the specific books and want to be suggested some books
    1. if users are finding some specific books and given retrieved rows includes the books, your response should be:
    Vâng, bên mình có cuốn sách (or truyện depending on Query) ...(Name of books that user expect), bạn có thể tham khảo qua! or Đây là danh sách sách các sách (or truyện depending on Query) liên quan đến ..(Name of books that user expect), mời bạn tham khảo.
    2. if users are finding some specific books and given retrieved rows not includes the books, your response should be:
    Xin lỗi, hiện tại bên mình đang không có sách (or truyện depending on Query) ...(Name of books that user expect) mà bạn đang cần, bạn có thể thử tìm sách khác hoặc mình có thể đề xuất cho bạn một số sách.
    3. if users dont find the specific books and want to be suggested some books, your response should be:
    Đây là một số sách (or truyện depending on Query) mình có thể đề xuất cho bạn.
    Then you can ask the user some other questions that the user might be interested in related to the question.
    Please note that you do not return any information related to the book in given retrieved rows
    Example:
    Query: Tôi muốn tìm truyện Doraemon
    Response: Đây là danh sách truyện Doraemon hiện tại chúng mình đang có, bạn có thể cho mình biết bạn đang muốn tìm tập truyện nào để mình tìm kiếm cho bạn
    
    Query: Tôi muốn tìm truyện Naruto"
    Response: Bên mình truyện Naruto hiện tại đang có rất nhiều, bạn có thể tham khảo qua, đồng thời truyện Naruto bên mình cũng đang ưu đãi giảm giá khá nhiều nhé!
    
    Query: Bạn có thể đề giới thiệu cho tôi một số truyện bạn đang có
    Response: Đây là một số truyện mình có thể đề xuất cho bạn, nếu bạn quan tâm đến sản phẩm nào có thể cho mình biết nhé!
    
    Response: 
    '''

    def answer_query(query_str: str) -> str:
        """
        A helpfull function to answer a book query.

        Args:
            query_str (str): The query string to search for.

        Returns:
            str: The answer to the query.
        """
        es_response = es.search(query_str)
        retrieved_rows = [{"id": node.id,
                           "URL": node.URL,
                           "title": node.title,
                           "current_price": node.current_price,
                           "original_price": node.original_price,
                           "img_url": node.img_url} 
                          for node in es_response]
        response = llm.complete(RESPONSE_SYNTHESIS_PROMPT.format(query_str=query_str, retrieved_rows=retrieved_rows))
        response_dict = {"rows": retrieved_rows, "response": str(response)}
        response_json = json.dumps(response_dict, ensure_ascii=False)
        return response_json

    return FunctionTool.from_defaults(
        fn=answer_query,
        return_direct=True,
        description="A useful tool to answer queries of user about book information.",
    )