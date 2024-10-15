from llama_index.core.bridge.pydantic import BaseModel
from sqlmodel import Field, SQLModel
import uuid as uuid_pkg


class RAGType:
    """
    RAG type schema.

    Attributes:
        ORIGIN (str): Origin RAG type.
        CONTEXTUAL (str): Contextual RAG type.
        BOTH (str): Both Origin and Contextual RAG type.
    """

    ORIGIN = "origin"
    CONTEXTUAL = "contextual"
    BOTH = "both"


class DocumentMetadata(BaseModel):
    """
    Document metadata schema.

    Attributes:
        doc_id (str): Document ID.
        original_content (str): Original content of the document.
        contextualized_content (str): Contextualized content of the document which will be prepend to the original content.
    """

    doc_id: str
    original_content: str
    contextualized_content: str


class DocElasticSearchResponse(BaseModel):
    """
    ElasticSearch response schema.

    Attributes:
        doc_id (str): Document ID.
        content (str): Content of the document.
        contextualized_content (str): Contextualized content of the document.
        score (float): Score of the document.
    """

    doc_id: str
    content: str
    contextualized_content: str
    score: float


class BookElasticSearchResponse(BaseModel):
    """
    ElasticSearch response schema.
    """

    id: str
    URL: str
    title: str
    current_price: int
    original_price: int
    img_url: str
    score: float


class Book3(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    URL: str = Field(
        ...,
        description="URL to the book",
    )
    title: str = Field(
        ...,
        description="Title of the book",
    )
    gift: str = Field(
        ...,
        description="Gift of the book",
    )
    description: str = Field(
        ...,
        description="Description of the book",
    )
    current_price: int = Field(
        ...,
        description="Current price of the book after sale",
    )
    original_price: int = Field(
        ...,
        description="Original price of the book",
    )
    sold: int = Field(
        ...,
        description="Number of copies sold",
    )
    authors: str = Field(
        ...,
        description="The authors of the book",
    )
    readers: str = Field(
        ...,
        description="Target audience of the book",
    )
    size: str = Field(
        ...,
        description="Width and height of the book in cm",
    )
    num_page: str = Field(
        ...,
        description="Number of book's pages",
    )
    cover_format: str = Field(
        ...,
        description="Format to book's cover, soft cover or hard cover",
    )
    weight: str = Field(
        ...,
        description="Weight of the book in gram",
    )
    book_set: str = Field(
        ...,
        description="Book set of the book",
    )
    img_url: str = Field(
        ...,
        description="URL to the book image",
    )
    dop: str = Field(
        ...,
        description="Date of publication of the book",
    )
    books_available: int = Field(
        ...,
        description="Number of the book in stock",
    )
