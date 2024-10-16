import sys
import pandas as pd
from tqdm import tqdm
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from sqlmodel import create_engine, Session, SQLModel, select
from src.settings import setting as config_setting
from src.schemas import Book3
from src.embedding.book_elastic_search import ElasticSearch
from decouple import config


SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

es = ElasticSearch(
    url=config_setting.elastic_search_url, index_name=config_setting.book_elastic_search_index_name
)


def convert_to_book_result(df: pd.DataFrame):
    data = []
    for _, row in df.iterrows():
        data.append(
            Book3(
                URL=row["URL"],
                title=row["title"],
                gift=row["gift"],
                description=row["description"],
                current_price=row["currentPrice"],
                original_price=row["originalPrice"],
                sold=row["sold"],
                authors=row["authors"],
                readers=row["readers"],
                size=row["size"],
                num_page=row["numPage"],
                cover_format=row["format"],
                weight=row["weight"],
                book_set=row["bookSet"],
                img_url=row["imgURL"],
                dop=row["dateOfPublication"],
                books_available=row["booksAvailable"]
            )
        )
    return data


def insert_to_db(file_path: Path):
    df = pd.read_csv(file_path)
    df.fillna('Không có', inplace=True)
    data = convert_to_book_result(df)

    with Session(engine) as session:
        for row in tqdm(data):
            session.add(row)
        session.commit()


def insert_to_es():
    books_metadata = []
    with Session(engine) as session:
        stmt = select(Book3)
        data = session.exec(stmt)
        for row in data:
            books_metadata.append(row)

    es.index_books(books_metadata)


def get_db_context(size: int = 5):
    result = []
    with Session(engine) as session:
        stmt = select(Book3).limit(size)
        data = session.exec(stmt)
        for row in data:
            result.append(row)

    table_columns = Book3.__table__.columns.keys()
    context_str = " | ".join(table_columns)
    # Make a context str for llm to understand
    for row in result:
        context_str += "\n"
        context_str += " | ".join([str(getattr(row, col)) for col in table_columns])

    return context_str


def init_db():
    SQLModel.metadata.create_all(engine)


# init_db()
# insert_to_db(r"D:\HK5\AIEngineer\Book_Selling_Assistant\backend\sample_data\sample_data5.csv")
# print(get_db_context())
#insert_to_es()
response = es.search("Tôi muốn tìm truyện Naruto 36")
print(response)
