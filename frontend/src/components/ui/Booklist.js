import React from 'react';

const Booklist = ({ selectedBooks }) => {
  return (
    <section className="py-5">
        <div className="container px-4 px-lg-5 mt-5">
            <div className="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
                {selectedBooks.map((book, index) => {
                    const bookTitle = book["Book-Title"];
                    const truncatedTitle = bookTitle.length > 35 ? bookTitle.substring(0, 35) + "..." : bookTitle;

                    return (
                        <div key={index} className="col mb-5">
                            <div className="card h-100">
                                <a href={book.url} className="image-container" style={{ textDecoration: 'none' }}>
                                    <img
                                    src={book["Image-URL-L"]}
                                    alt="No find image"
                                    />
                                </a>
                                <div
                                    className="badge bg-dark text-white position-absolute"
                                    style={{ top: "0.5rem", right: "0.5rem" }}
                                >
                                    Kết quả
                                </div>
                                <div className="card-body p-4">
                                    <div className="text-center">
                                    <h5 className="fw-bolder">{truncatedTitle}</h5>
                                    <span className="text-muted text-decoration-line-through">
                                        {new Intl.NumberFormat('vi-VN').format('100000')}₫
                                    </span>
                                    {new Intl.NumberFormat('vi-VN').format('80000')}₫
                                    </div>
                                </div>
                                <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                    <div className="text-center">
                                    <a className="btn btn-outline-dark mt-auto" href="/">
                                        Thêm vào giỏ hàng
                                    </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    </section>
  );
};

export default Booklist;