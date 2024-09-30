import React from 'react';
import backgroundImage from '../../assets/1333324.png';

const Header = () => {
  return (
    <header
        className="bg-dark py-5"
        style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "center"
        }}
        >
        <div className="container px-4 px-lg-5 my-5">
            <div className="text-center text-white">
            <h1 className="display-4 fw-bolder">CS311 Store</h1>
            <p className="lead fw-normal mb-0">Tìm kiếm và gợi ý sách với GenAI</p>
            </div>
        </div>
    </header>
  );
};

export default Header;