import psycopg2


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


def main():
    print("Validating database...")

    connection = connect_to_database()

    validate_row_counts(connection)

    connection.close()

    print("Validation complete.")


if __name__ == "__main__":
    main()