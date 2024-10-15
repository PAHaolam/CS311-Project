from icecream import ic
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from llama_index.core.bridge.pydantic import Field

from src.schemas import BookElasticSearchResponse, Book3


class ElasticSearch:
    """
    ElasticSearch client to index and search books for contextual RAG.
    """

    url: str = Field(..., description="Elastic Search URL")

    def __init__(self, url: str, index_name: str):
        """
        Initialize the ElasticSearch client.

        Args:
            url (str): URL of the ElasticSearch server
            index_name (str): Name of the index used to be created for contextual RAG
        """
        ic(url, index_name)

        self.es_client = Elasticsearch(url)
        self.index_name = index_name
        self.create_index()

    def create_index(self):
        """
        Create the index for contextual RAG from provided index name.
        """
        index_settings = {
            "settings": {
                "analysis": {"analyzer": {"default": {"type": "standard"}}},
                "similarity": {"default": {"type": "BM25"}},
                "index.queries.cache.enabled": False,  # Disable query cache
            },
            "mappings": {
                "properties": {
                    "URL": {"type": "keyword"},  # Không phân tích, dùng để truy vấn trực tiếp
                    "title": {"type": "text", "analyzer": "standard"},  # Phân tích để tìm kiếm toàn văn bản
                    "gift": {"type": "keyword"},  # Trường ngắn, không cần phân tích
                    "description": {"type": "text", "analyzer": "standard"},  # Phân tích mô tả
                    "current_price": {"type": "integer"},  # Số thực
                    "original_price": {"type": "integer"},  # Số thực
                    "sold": {"type": "integer"},  # Số lượng bán
                    "authors": {"type": "text", "analyzer": "standard"},  # Phân tích tác giả
                    "readers": {"type": "text", "analyzer": "standard"},  # Đối tượng độc giả
                    "book_set": {"type": "text", "analyzer": "standard"},  # Tên bộ sách
                    "img_url": {"type": "keyword"},  # URL ảnh
                    "dop": {"type": "date", "format": "yyyy-MM-dd"},  # Ngày phát hành
                    "books_available": {"type": "integer"},  # Số lượng sách có sẵn
                    "book_id": {"type": "text", "index": False}
                }
            },
        }

        if not self.es_client.indices.exists(index=self.index_name):
            self.es_client.indices.create(index=self.index_name, body=index_settings)
            ic(f"Created index: {self.index_name}")

    def index_books(self, books_metadata: list[Book3]) -> bool:
        """
        Index the books to the ElasticSearch index.

        Args:
            books_metadata (list[Book3]): List of books metadata to index.
        """
        ic("Indexing books...")

        actions = [
            {
                "_index": self.index_name,
                "_source": {
                    "book_id": str(getattr(metadata, "id")),
                    "URL": getattr(metadata, "URL"),
                    "title": getattr(metadata, "title"),
                    "gift": getattr(metadata, "gift"),
                    "description": getattr(metadata, "description"),
                    "current_price": getattr(metadata, "current_price"),
                    "original_price": getattr(metadata, "original_price"),
                    "sold": getattr(metadata, "sold"),
                    "authors": getattr(metadata, "authors"),
                    "readers": getattr(metadata, "readers"),
                    "book_set": getattr(metadata, "book_set"),
                    "img_url": getattr(metadata, "img_url"),
                    "dop": getattr(metadata, "dop"),
                    "books_available": getattr(metadata, "books_available"),
                },
            }
            for metadata in books_metadata
        ]

        success, _ = bulk(self.es_client, actions)
        if success:
            ic("Indexed documents successfully !")

        self.es_client.indices.refresh(index=self.index_name)

        return success

    def search(self, query: str, k: int = 20) -> list[BookElasticSearchResponse]:
        """
        Search the books relevant to the query.

        Args:
            query (str): Query to search
            k (int): Number of books to return

        Returns:
            list[ElasticSearchResponse]: List of ElasticSearch response objects.
        """
        ic(query, k)

        self.es_client.indices.refresh(
            index=self.index_name
        )  # Force refresh before each search
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "gift", "description", "img_url", "authors", "readers", "book_set"],
                }
            },
            "size": k,
        }
        response = self.es_client.search(index=self.index_name, body=search_body)

        return [
            BookElasticSearchResponse(
                id=hit["_source"]["book_id"],
                URL=hit["_source"]["URL"],
                title=hit["_source"]["title"],
                current_price=hit["_source"]["current_price"],
                original_price=hit["_source"]["original_price"],
                img_url=hit["_source"]["img_url"],
                score=hit["_score"],
            )
            for hit in response["hits"]["hits"]
        ]
