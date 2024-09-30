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

import React, { useState } from 'react';
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

  const handleSendMessage = async () => {
    if(inputValue===''){
      return;
    }
    setContentChatbox(prevContent => prevContent.concat({ "typeChat": "sent", "contentChat": inputValue }));
    setInputValue('');  // Xóa nội dung trong ô input sau khi gửi
    try{
      const response = await api.post('/chat', { message: inputValue });
      //console.log(response.data.answer)
      setContentChatbox(prevContent => prevContent.concat({ "typeChat": "received", "contentChat": response.data.answer }));
    } catch (error) {
      console.error("Error fetching API response:", error);
      setContentChatbox(prevContent => prevContent.concat({ "typeChat": "received", "contentChat": "Đang xảy ra vấn đề khi kết nối với chatbot, bạn vui lòng trở lại sau nhé, xin cảm ơn!" }));
    }
  };

  return (
    <div className="App">
      <Narbar openChatbox={openChatbox} />
      <Header />
      <Chatbox show={showChatbox} closeChatbox={closeChatbox} content={contentChatbox} inputValue={inputValue} handleInputChange={handleInputChange} handleSendMessage={handleSendMessage}/>
      <Booklist />
    </div>
  );
}

export default App;
