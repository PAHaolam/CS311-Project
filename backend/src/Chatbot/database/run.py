import sys
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import ast

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from sqlmodel import create_engine, Session, SQLModel, select
from Chatbot.settings import setting
from Chatbot.database.schema import Book, Size


SQLALCHEMY_DATABASE_URL = setting.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def extract_size(row) -> Size:
    size = row[9][1:-1].split(", ")
    return Size(width=float(size[0]), height=float(size[1]))


def concat_authors(row) -> str:
    author_list = ast.literal_eval(row[6])
    return " & ".join(author_list)


def concat_age_reader(row) -> str:
    age_reader_list = ast.literal_eval(row[7])
    return " & ".join(age_reader_list)


def convert_to_book_result(df: pd.DataFrame):
    data = []
    for _, row in df.iterrows():
        size = extract_size(row)
        authors=concat_authors(row)
        age_reader=concat_age_reader(row)
        data.append(
            Book(
                url=row[0],  # URL của trang sách
                title=row[1],  # Tiêu đề sách
                description=row[2],  # Mô tả sách
                current_price=row[3],  # Giá hiện tại
                original_price=row[4],  # Giá gốc
                sold=row[5],  # Số lượng đã bán
                authors=authors,  # Danh sách tác giả
                age_reader=age_reader,  # Độ tuổi độc giả
                gift=row[8],  # Quà tặng kèm
                width=size.width,  # Chiều rộng sách
                height=size.height,  # Chiều dài sách
                num_page=row[10],  # Số trang
                format=row[11],  # Định dạng sách (bìa mềm, bìa cứng, ...)
                weight=row[12],  # Trọng lượng sách
            )
        )
    return data


def insert_to_db(file_path: Path):
    df = pd.read_csv(file_path)
    data = convert_to_book_result(df)

    with Session(engine) as session:
        for row in tqdm(data):
            session.add(row)
        session.commit()


def get_db_context(size: int = 5):
    result = []
    with Session(engine) as session:
        stmt = select(Book).limit(size)
        data = session.exec(stmt)
        for row in data:
            result.append(row)

    table_columns = Book.__table__.columns.keys()
    context_str = " | ".join(table_columns)
    # Make a context str for llm to understand
    for row in result:
        context_str += "\n"
        context_str += " | ".join([str(getattr(row, col)) for col in table_columns])

    return context_str


def init_db():
    SQLModel.metadata.create_all(engine)

#init_db()
#insert_to_db(r"D:\HK5\AI Engineer\Book_Selling_Assistant\backend\src\data\sample_data.csv")
#print(get_db_context())
