from sqlmodel import Field, SQLModel
import uuid as uuid_pkg


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
