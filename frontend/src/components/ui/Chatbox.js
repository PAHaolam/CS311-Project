import React, { useEffect, useRef } from 'react';

const Chatbox = ({ show, closeChatbox, content, inputValue, handleInputChange, handleSendMessage, responseWaiting }) => {
  // Tạo ref để tham chiếu đến div chatbox-messages
  const messagesEndRef = useRef(null);

  // Sử dụng useEffect để cuộn xuống đáy mỗi khi content thay đổi
  useEffect(() => {
    // Khi content cập nhật, cuộn xuống đáy
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [content, responseWaiting]); // Mỗi khi content thay đổi, useEffect sẽ được kích hoạt

  return (
    <>
      {show && (
        <div className="chatbox">
            <div className="chatbox-header">
                <svg 
                    xmlns="http://www.w3.org/2000/svg"
                    width={20}
                    height={20}
                    fill="currentColor"
                    className="bi bi-robot"
                    viewBox="0 0 16 16"
                >
                    <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135" />
                    <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5" />
                </svg>
                <button className="close-btn" onClick={closeChatbox}>
                    ×
                </button>
            </div>
            <div className="chatbox-messages">
                {
                  content.map((message, index) => {
                    return (
                      <div key={index} className={`message ${message.typeChat}`}>
                        <div className="content">
                          {message.contentChat}
                        </div>
                      </div>
                    );
                  })
                }
                {
                  responseWaiting && (
                    <div className={'message received'}>
                      <div className="content">
                        {/* {message.contentChat} */}
                        <div class="bouncing-dots">
                          <div class="dot"></div>
                          <div class="dot"></div>
                          <div class="dot"></div>
                        </div>
                      </div>
                    </div>
                  )
                }
                <div ref={messagesEndRef} />
            </div>
            <div className="chatbox-input">
                <input 
                  type="text" 
                  placeholder="Bạn muốn tìm gì ?" 
                  value={inputValue} 
                  onChange={handleInputChange}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        handleSendMessage(); // Gọi hàm khi nhấn Enter
                    }
                }}
                />
                <button onClick={handleSendMessage}>📨</button>
            </div>
        </div>
      )}
    </>
  );
};

export default Chatbox;
