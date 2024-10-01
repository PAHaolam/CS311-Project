from sqlmodel import Field, SQLModel
from typing import List, Optional
from pydantic import BaseModel
import uuid as uuid_pkg


class Size(BaseModel):
    width: float
    height: float


class Book(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    url: str = Field(
        ...,
        description="URL to the book page",
    )
    title: str = Field(
        ...,
        description="Title of the book",
    )
    description: str = Field(
        description="Description of transaction",
        default="",
    )
    current_price: float = Field(
        ...,
        description="Current selling price of the book",
    )
    original_price: float = Field(
        ...,
        description="Original price of the book",
    )
    sold: int = Field(
        ...,
        description="Number of copies sold",
    )
    authors: str = Field(
        ...,
        description="List of authors of the book",
    )
    age_reader: str = Field(
        ...,
        description="Target reader age group",
    )
    gift: Optional[str] = Field(
        default="Không có",
        description="Any included gifts with the book",
    )
    width: float = Field(
        ...,
        description="Dimensions of the book width in cm",
    )
    height: float = Field(
        ...,
        description="Dimensions of the book height in cm",
    )
    num_page: int = Field(
        ...,
        description="Number of pages in the book",
    )
    format: str = Field(
        ...,
        description="Book format, e.g., softcover or hardcover",
    )
    weight: float = Field(
        ...,
        description="Weight of the book in grams",
    )
