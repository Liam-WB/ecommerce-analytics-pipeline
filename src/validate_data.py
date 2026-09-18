import psycopg2


VALID_STATUSES = {
    "Delivered",
    "Processing",
    "Sent",
    "Cancelled",
}


def connect_to_database():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="ecommerce_analytics",
        user="ecommerce_user",
        password="ecommerce_password",
    )


def validate_row_counts(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers;")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products;")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders;")
    order_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_items;")
    order_item_count = cursor.fetchone()[0]

    print(f"Customers: {customer_count}")
    print(f"Products: {product_count}")
    print(f"Orders: {order_count}")
    print(f"Order items: {order_item_count}")

    cursor.close()


def validate_customer_references(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL;
    """)

    invalid_orders = cursor.fetchone()[0]

    if invalid_orders == 0:
        print("✓ All orders have valid customers")
    else:
        print(f"✗ Found {invalid_orders} orders with invalid customers")

    cursor.close()


def validate_product_references(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN products p
            ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL;
    """)

    invalid_items = cursor.fetchone()[0]

    if invalid_items == 0:
        print("✓ All order items have valid products")
    else:
        print(f"✗ Found {invalid_items} order items with invalid products")

    cursor.close()


def validate_quantities(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE quantity <= 0;
    """)

    invalid_quantities = cursor.fetchone()[0]

    if invalid_quantities == 0:
        print("✓ All quantities are valid")
    else:
        print(f"✗ Found {invalid_quantities} invalid quantities")

    cursor.close()


def validate_prices(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE unit_price <= 0;
    """)

    invalid_prices = cursor.fetchone()[0]

    if invalid_prices == 0:
        print("✓ All unit prices are valid")
    else:
        print(f"✗ Found {invalid_prices} invalid unit prices")

    cursor.close()


def validate_customer_emails(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
        WHERE email IS NULL
           OR TRIM(email) = '';
    """)

    missing_emails = cursor.fetchone()[0]

    if missing_emails == 0:
        print("✓ All customers have an email")
    else:
        print(f"✗ Found {missing_emails} customers with missing emails")

    cursor.close()


def validate_duplicate_emails(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT email
            FROM customers
            GROUP BY email
            HAVING COUNT(*) > 1
        ) duplicates;
    """)

    duplicate_emails = cursor.fetchone()[0]

    if duplicate_emails == 0:
        print("✓ No duplicate customer emails found")
    else:
        print(f"✗ Found {duplicate_emails} duplicate email groups")

    cursor.close()


def validate_order_statuses(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status NOT IN (
            'Delivered',
            'Processing',
            'Sent',
            'Cancelled'
        );
    """)

    invalid_statuses = cursor.fetchone()[0]

    if invalid_statuses == 0:
        print("✓ All order statuses are valid")
    else:
        print(f"✗ Found {invalid_statuses} invalid order statuses")

    cursor.close()


def validate_order_dates(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE order_date IS NULL;
    """)

    invalid_dates = cursor.fetchone()[0]

    if invalid_dates == 0:
        print("✓ All orders have a date")
    else:
        print(f"✗ Found {invalid_dates} orders with missing dates")

    cursor.close()


def validate_orders_have_items(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders o
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE oi.order_id IS NULL;
    """)

    empty_orders = cursor.fetchone()[0]

    if empty_orders == 0:
        print("✓ All orders contain order items")
    else:
        print(f"✗ Found {empty_orders} orders without order items")

    cursor.close()


def main():
    print("Validating database...")
    print()

    connection = connect_to_database()

    validate_row_counts(connection)
    validate_customer_references(connection)
    validate_product_references(connection)
    validate_quantities(connection)
    validate_prices(connection)
    validate_customer_emails(connection)
    validate_duplicate_emails(connection)
    validate_order_statuses(connection)
    validate_order_dates(connection)
    validate_orders_have_items(connection)

    connection.close()

    print()
    print("Validation complete.")


if __name__ == "__main__":
    main()