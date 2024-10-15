from config.config import get_config

cfg = get_config("QdrantElasticAgent/config/config.yaml")
cfg.merge_from_file("QdrantElasticAgent/config/postgres.yaml")


STREAM = cfg.MODEL.STREAM
SERVICE = cfg.MODEL.SERVICE
TEMPERATURE = cfg.MODEL.TEMPERATURE
MODEL_ID = cfg.MODEL.MODEL_ID


CONTEXTUAL_PROMPT = """<document>
{WHOLE_DOCUMENT}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{CHUNK_CONTENT}
</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else."""

QA_PROMPT = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question: {query_str}\n"
    "If this information is about ISBN (e.g: 067176537X, 3404921038, ...) or title of a book or list of books, you will define whether if users are finding some specific books or users dont find the specific books and want to be suggested some books\n"
    "1. if users are finding some specific books, your response should be:\n"
    "'Vâng, chúng tôi có cuốn sách ... (Name of books that user expect), bạn có thể tham khảo qua!' or 'Đây là danh sách sách các sách liên quan đến ... (Name of books that user expect), mời bạn tham khảo' if given information includes the books\n"
    "'Xin lỗi, hiện tại bên chúng tôi đang không có sách mà bạn đang cần, bạn có thể thử tìm sách khác hoặc chúng tôi có thể đề xuất cho bạn một số sách' if given information not includes the books\n"
    "2. if users dont find the specific books and want to be suggested some books, your response should be:\n"
    "'Đây là một số sách tôi có thể đề xuất cho bạn'\n"
    "please return your response exactly in the format:\n"
    "{{'response': <your response>, 'book_list': <list of ISBN of books in given information>\}} notice that if there is no book in given information, please return the empty list\n"
)

FORMATTING_PROMPT = '''
We have provided the message below.
---------------------
{response}
---------------------
If this message includes ISBN of a book or list of books, you will separate ISBNs and the main content of given message into two parts.
Then you will return your response exactly in the format:
{{'response': <the main content of given message>, 'book_list': <list of ISBNs in given message>\}} notice that if there is no book in given information, please return the empty list

Example:
Message: Dưới đây là một số sách mà tôi có thể đề xuất cho bạn:\n\n1. 067176537X\n2. 3404921038\n3. 0375759778\n4. 0425163091\n5. 3442353866\n6. 3442410665\n7. 3442446937\n8. 0375406328\n9. 0446310786\n10. 0449005615\n\nNếu bạn cần thông tin chi tiết hơn về bất kỳ cuốn sách nào, hãy cho tôi biết!
Your response: {{'response': 'Đây là một số sách mà tôi có thể đề xuất cho bạn, nếu bạn cần thông tin chi tiết hơn về bất kỳ cuốn sách nào, hãy cho tôi biết!', 'book_list': ['067176537X', '3404921038', '0375759778', '0425163091', '3442353866', '3442410665', '3442446937', '0375406328', '0446310786', '0449005615']}}
'''

# Contextual RAG
CONTEXTUAL_CHUNK_SIZE = cfg.CONTEXTUAL_RAG.CHUNK_SIZE
CONTEXTUAL_SERVICE = cfg.CONTEXTUAL_RAG.SERVICE
CONTEXTUAL_MODEL = cfg.CONTEXTUAL_RAG.MODEL

ORIGINAL_RAG_COLLECTION_NAME = cfg.CONTEXTUAL_RAG.ORIGIN_RAG_COLLECTION_NAME
CONTEXTUAL_RAG_COLLECTION_NAME = cfg.CONTEXTUAL_RAG.CONTEXTUAL_RAG_COLLECTION_NAME

QDRANT_URL = cfg.CONTEXTUAL_RAG.QDRANT_URL
ELASTIC_SEARCH_URL = cfg.CONTEXTUAL_RAG.ELASTIC_SEARCH_URL
DOC_ELASTIC_SEARCH_INDEX_NAME = cfg.CONTEXTUAL_RAG.DOC_ELASTIC_SEARCH_INDEX_NAME
BOOK_ELASTIC_SEARCH_INDEX_NAME = cfg.CONTEXTUAL_RAG.BOOK_ELASTIC_SEARCH_INDEX_NAME

NUM_CHUNKS_TO_RECALL = cfg.CONTEXTUAL_RAG.NUM_CHUNKS_TO_RECALL
SEMANTIC_WEIGHT = cfg.CONTEXTUAL_RAG.SEMANTIC_WEIGHT
BM25_WEIGHT = cfg.CONTEXTUAL_RAG.BM25_WEIGHT
TOP_N = cfg.CONTEXTUAL_RAG.TOP_N

SUPPORTED_FILE_EXTENSIONS = [".pdf", ".docx", ".csv", ".html", ".xlsx", ".json", ".txt"]

AGENT_TYPE = cfg.AGENT.TYPE
