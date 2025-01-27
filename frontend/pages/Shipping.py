import streamlit as st
import sidebar as sidebar
import pandas as pd
import ast
from pathlib import Path

# Đọc tệp TXT
def read_file(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            timestamp, raw_info = line.split(" : ", 1)
            info = ast.literal_eval(raw_info.strip())  # Chuyển chuỗi thành dict
            info['timestamp'] = timestamp
            data.append(info)
    return data

# Hiển thị thông tin trong Streamlit
def display_data(data):
    st.title("Thông Tin đặt hàng")

    # Đường dẫn đến tệp TXT
    current_dir = Path(__file__).resolve().parent.parent
    file_path = current_dir.parent / "backend" / "RAG_tool" / "data" / "sample_data5.csv"
    df_product = pd.read_csv(file_path)
    for entry in data[::-1]:
        st.subheader(f"Thời gian: {entry['timestamp']}")
        st.write(f"**Tên**: {entry['name']}")
        st.write(f"**Số điện thoại**: {entry['phone']}")
        st.write(f"**Địa chỉ**: {entry['address']}")
        st.write("**Danh sách sách:**")
        total_price = 0  # Biến lưu tổng tiền
        for book, quantity in entry['book_list']:
            # Lọc dòng có title chứa tên sách
            matching_books = df_product[df_product['title'] == book]
            if not matching_books.empty:
                price = matching_books['currentPrice'].iloc[0]  # Lấy giá của sách
                price = int(price)
                total_price += price * quantity  # Tính tổng tiền
                st.write(f"- {book} (Số lượng: {quantity}, Giá: {price:,} đ)")  # Hiển thị giá sách
        
        # Hiển thị tổng tiền
        st.write(f"**Tổng tiền**: {total_price:,} đ")
        st.write("---")  # Đường phân cách


def main():
    sidebar.show_sidebar()

    # Đường dẫn đến tệp TXT
    current_dir = Path(__file__).resolve().parent.parent
    file_path = current_dir.parent / "backend" / "RAG_tool" / "data" / "orders.txt"

    # Đọc và hiển thị dữ liệu
    data = read_file(file_path)
    display_data(data)

    

if __name__ == "__main__":
    main()