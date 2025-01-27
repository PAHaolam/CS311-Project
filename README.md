tạo file backend/.env lưu 2 biến OPENAI_API_KEY và LANGCHAIN_API_KEY

tải thư viện cần thiết: 
<pre> <code>pip install -r requirements.txt</code></pre>

chạy backend:
<pre> <code>cd backend</code></pre>
<pre> <code>uvicorn main:app --reload</code></pre>

chạy frontend:
<pre> <code>cd frontend</code></pre>
<pre> <code>streamlit run Home.py</code></pre>


