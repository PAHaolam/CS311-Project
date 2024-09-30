import React from 'react';

const Header = () => {
  return (
    <section className="py-5">
        <div className="container px-4 px-lg-5 mt-5">
            <div className="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
                <div className="col mb-5">
                    <div className="card h-100">
                    <div className="image-container">
                        <img
                        src="https://dummyimage.com/960x1280"
                        alt="..."
                        />
                    </div>
                    <div
                        className="badge bg-dark text-white position-absolute"
                        style={{ top: "0.5rem", right: "0.5rem" }}
                    >
                        Bán chạy nhất
                    </div>
                    <div className="card-body p-4">
                        <div className="text-center">
                        <h5 className="fw-bolder">"Cậu" ma nhà xí Hanako - Tập 11</h5>
                        <span className="text-muted text-decoration-line-through">
                            50,000₫
                        </span>
                        45,000₫
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
                <div className="col mb-5">
                    <div className="card h-100">
                    <div className="image-container">
                        <img
                        src="https://dummyimage.com/960x1280"
                        alt="..."
                        />
                    </div>
                    <div
                        className="badge bg-dark text-white position-absolute"
                        style={{ top: "0.5rem", right: "0.5rem" }}
                    >
                        Mới nhất
                    </div>
                    <div className="card-body p-4">
                        <div className="text-center">
                        <h5 className="fw-bolder">"Nhóc Maruko - Tập 12</h5>
                        <span className="text-muted text-decoration-line-through">
                            40,000₫
                        </span>
                        36,000₫
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
                <div className="col mb-5">
                    <div className="card h-100">
                    <div className="image-container">
                        <img
                        src="https://dummyimage.com/960x1280"
                        alt="..."
                        />
                    </div>
                    <div
                        className="badge bg-dark text-white position-absolute"
                        style={{ top: "0.5rem", right: "0.5rem" }}
                    >
                        Hết hàng
                    </div>
                    <div className="card-body p-4">
                        <div className="text-center">
                        <h5 className="fw-bolder">Chú thuật hồi chiến - Tập 1</h5>
                        <span className="text-muted text-decoration-line-through">
                            30,000₫
                        </span>
                        27,000₫
                        </div>
                    </div>
                    <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                        <div className="text-center">
                        <a
                            className="btn btn-outline-dark mt-auto"
                            style={{
                            borderColor: "red",
                            backgroundColor: "red",
                            color: "white"
                            }}
                            href="/"
                        >
                            Tạm hết hàng
                        </a>
                        </div>
                    </div>
                    </div>
                </div>
                <div className="col mb-5">
                    <div className="card h-100">
                    <div className="image-container">
                        <img
                        src="https://dummyimage.com/960x1280"
                        alt="..."
                        />
                    </div>
                    <div
                        className="badge bg-dark text-white position-absolute"
                        style={{ top: "0.5rem", right: "0.5rem" }}
                    >
                        Hết hàng
                    </div>
                    <div className="card-body p-4">
                        <div className="text-center">
                        <h5 className="fw-bolder">Chú thuật hồi chiến - Tập 2</h5>
                        <span className="text-muted text-decoration-line-through">
                            30,000₫
                        </span>
                        27,000₫
                        </div>
                    </div>
                    <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                        <div className="text-center">
                        <a
                            className="btn btn-outline-dark mt-auto"
                            style={{
                            borderColor: "red",
                            backgroundColor: "red",
                            color: "white"
                            }}
                            href="/"
                        >
                            Tạm hết hàng
                        </a>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

  );
};

export default Header;