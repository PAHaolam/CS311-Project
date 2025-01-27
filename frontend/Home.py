import streamlit as st
import sidebar as sidebar
import webbrowser
import requests

# Hàm gọi API
def fetch_books():
    url = "http://127.0.0.1:8000/v1/init_books"  # URL của API FastAPI
    try:
        response = requests.post(url)  # Gửi yêu cầu POST
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Chuyển đổi phản hồi JSON thành dictionary
        return data.get("books", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching books: {e}")
        return []

def main():
    sidebar.show_sidebar()

    # Gọi API và lấy dữ liệu
    books = fetch_books()

    # Hiển thị danh sách sách
    if books:
        # Chia thành các dòng, mỗi dòng chứa 4 quyển sách
        newest_books = books[:12]
        trending_books = books[12:]

        st.info("Mới nhất")
        for i in range(0, len(newest_books), 4):
            cols = st.columns(4)  # Tạo 4 cột
            for col, book in zip(cols, newest_books[i:i + 4]):
                with col:
                    st.image(book['img_url'], use_container_width=True)
                    st.markdown(f"### {book['title']}")
                    st.write(f"**Giá:** {book['current_price']}")
                    st.write(f"**~~{book['original_price']}~~")
                    st.write(f"[Xem chi tiết]({book['URL']})")

        st.info("Bán chạy nhất")
        for i in range(0, len(trending_books), 4):
            cols = st.columns(4)  # Tạo 4 cột
            for col, book in zip(cols, trending_books[i:i + 4]):
                with col:
                    st.image(book['img_url'], use_container_width=True)
                    st.markdown(f"### {book['title']}")
                    st.write(f"**Giá hiện tại:** {book['current_price']}")
                    st.write(f"**Giá gốc:** {book['original_price']}")
                    st.write(f"[Xem chi tiết]({book['URL']})")

    else:
        st.info("Không có sách để hiển thị.")

if __name__ == "__main__":
    main()