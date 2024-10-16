// import React from "react";
// import QuestionForm from "./Chatbot";

// function App() {
//   return (
//     <div>
//       <h1>Chatbot</h1>
//       <QuestionForm />
//     </div>
//   );
// }

// export default App;

import React, { useState, useEffect } from 'react';
import Narbar from './components/ui/Navbar';
import Header from './components/ui/Header';
import Chatbox from './components/ui/Chatbox';
import Booklist from './components/ui/Booklist';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

function App() {
  const [showChatbox, setShowChatbox] = useState(false);
  const [contentChatbox, setContentChatbox] = useState([{"typeChat": "received", "contentChat": "Xin chào! tôi là trợ lý bán sách, hãy nhập thông tin về sách bạn mong muốn, tôi sẽ giúp giúp bạn tìm kiếm hoặc đưa ra gợi ý cho bạn"}])
  const [inputValue, setInputValue] = useState('');  // State để lưu trữ giá trị của input
  const [selectedBooks, setSelectedBooks] = useState([])
  const [responseWaiting, setResponseWaiting] = useState(false)

  const openChatbox = (event) => {
    event.preventDefault();
    setShowChatbox(true);
  };

  const closeChatbox = () => {
    setShowChatbox(false);
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);  // Cập nhật state khi người dùng nhập
  };

  const updateBooks = (books, k) => {
    // Hàm đệ quy để cập nhật danh sách sách mỗi 200ms
    if (k <= books.length) {
      setSelectedBooks(books.slice(0, k)); // Lấy k phần tử đầu tiên
      setTimeout(() => {
        updateBooks(books, k + 1); // Tăng k và gọi lại sau 200ms
      }, 300); // 200ms
    }
  };

  const initBooks = async () => {
    try{
      const init_books = await api.post('/v1/init_books');
      setSelectedBooks(init_books.data.books)
    } catch (error) {
      console.error("Error fetching API response:", error);
    }
  }
  // useEffect ensures the function is called once when the component mounts
  useEffect(() => {
    initBooks();
  }, []); // Empty dependency array ensures it runs only once

  const handleSendMessage = async () => {
    if(inputValue===''){
      return;
    }
    setContentChatbox(prevContent => prevContent.concat({ "typeChat": "sent", "contentChat": inputValue }));
    setInputValue('');  // Xóa nội dung trong ô input sau khi gửi
    setTimeout(async () => {
      setResponseWaiting(true)
      try{
        let response = await api.post('/v1/complete', { message: inputValue });
      
        setResponseWaiting(false)
        setContentChatbox(prevContent => prevContent.concat({ "typeChat": "received", "contentChat": response.data.response }));
        if(response.data.books.length>0){
          updateBooks(response.data.books, 1);
        }
        // console.log(response.data.books)
      } catch (error) {
        console.error("Error fetching API response:", error);
        setResponseWaiting(false)
        setContentChatbox(prevContent => prevContent.concat({ "typeChat": "received", "contentChat": "Đang xảy ra vấn đề khi kết nối với chatbot, bạn vui lòng trở lại sau nhé, xin cảm ơn!" }));
      }
    }, 1000);
  };

  return (
    <div className="App">
      <Narbar openChatbox={openChatbox} />
      <Header />
      <Chatbox show={showChatbox} closeChatbox={closeChatbox} content={contentChatbox} inputValue={inputValue} handleInputChange={handleInputChange} handleSendMessage={handleSendMessage} responseWaiting={responseWaiting}/>
      <Booklist selectedBooks={selectedBooks}/>
    </div>
  );
}

export default App;
