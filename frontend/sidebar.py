import streamlit as st

def show_sidebar():
    st.sidebar.image("images/logo.jpg", use_column_width=True)
    st.sidebar.markdown('### Hệ thống Bán hàng sách tích hợp Chatbot tư vấn khách hàng.')

    st.sidebar.markdown('Hướng dẫn sử dụng:')
    st.sidebar.markdown('1. 📊 **Tham khảo danh sách những sách hiện đang có của chúng tôi bằng chức năng "Tham khảo sách".**')
    st.sidebar.markdown('2. 💬 **Sử dụng chức năng "Chatbot hỗ trợ" để nhắn tin với AI về thông tin sách và lên đơn đặt hàng.**')
    st.sidebar.markdown('3. 📈 **Thông tin đơn hàng của bạn sẽ được lưu lại. Bạn có thể sử dụng chức năng "Theo dõi đơn hàng" để xem chi tiết về thông tin đơn hàng của mình.**')
    st.sidebar.markdown('📝 Đồ án CS311.')