INSERT INTO customers (first_name, last_name, email, country, signup_date)
VALUES
    ('John', 'Smith', 'john.smith@example.com', 'UK', '2024-01-15'),
    ('Sarah', 'Jones', 'sarah.jones@example.com', 'UK', '2024-02-20'),
    ('Michael', 'Brown', 'michael.brown@example.com', 'USA', '2024-03-10'),
    ('Emma', 'Wilson', 'emma.wilson@example.com', 'Canada', '2024-04-05'),
    ('David', 'Taylor', 'david.taylor@example.com', 'UK', '2024-05-12');

INSERT INTO products (name, category, price, cost)
VALUES
    ('carrot', 'vegetables', 0.50, 0.30),
    ('apple', 'fruit', 0.80, 0.40),
    ('milk', 'dairy', 1.50, 0.90),
    ('bread', 'bakery', 1.20, 0.60),
    ('chicken breast', 'meat', 6.50, 4.00);

INSERT INTO orders (customer_id, order_date, status)
VALUES
    (1, '2026-04-27', 'Sent'),
    (2, '2026-04-28', 'Sent'),
    (3, '2026-05-03', 'Processing'),
    (4, '2026-05-10', 'Delivered'),
    (5, '2026-05-15', 'Cancelled');

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
    (1, 4, 2, 1.20),
    (2, 1, 3, 0.50),
    (3, 5, 1, 6.50),
    (4, 2, 4, 0.80),
    (5, 3, 2, 1.50);