Extract daily sales data from a database.
Generate daily report at 6 AM for previous day.

Database - Sales

CREATE TABLE sales (
    sid BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    order_number INT NOT NULL,
    article VARCHAR(80) NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    unit_price DOUBLE PRECISION NOT NULL
);
