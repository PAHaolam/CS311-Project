import React from 'react';

const Narbar = ({ openChatbox }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container px-4 px-lg-5">
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4">
            </ul>
            <form className="d-flex">
                <button
                className="btn btn-outline-dark"
                type="submit"
                onClick={openChatbox}
                //onclick="showChatBot(event)"
                >
                <i className="bi-cart-fill me-1" />
                Tìm kiếm
                </button>
                <button className="btn btn-outline-dark" type="submit">
                <i className="bi-cart-fill me-1" />
                Giỏ hàng
                <span className="badge bg-dark text-white ms-1 rounded-pill">0</span>
                </button>
                <button className="btn btn-outline-dark" type="submit">
                <i className="bi-cart-fill me-1" />
                Đơn hàng
                <span className="badge bg-dark text-white ms-1 rounded-pill">0</span>
                </button>
            </form>
            </div>
        </div>
    </nav>
  );
};

export default Narbar;