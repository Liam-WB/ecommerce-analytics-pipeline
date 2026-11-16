
import psycopg2
import csv


def connect_to_database():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="ecommerce_analytics",
        user="ecommerce_user",
        password="ecommerce_password",
    )


def load_csv(filepath):
    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def insert_customers(connection, customers):
    cursor = connection.cursor()

    try:
        for customer in customers:
            cursor.execute("""
                INSERT INTO customers (
                    customer_id,
                    first_name,
                    last_name,
                    email,
                    country,
                    signup_date
                )
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                customer["customer_id"],
                customer["first_name"],
                customer["last_name"],
                customer["email"],
                customer["country"],
                customer["signup_date"],
            ))

        print(f"Inserted {len(customers)} customers.")

    finally:
        cursor.close()


def insert_products(connection, products):
    cursor = connection.cursor()

    try:
        for product in products:
            cursor.execute("""
                INSERT INTO products (
                    product_id,
                    name,
                    category,
                    price,
                    cost
                )
                VALUES (%s, %s, %s, %s, %s);
            """, (
                product["product_id"],
                product["name"],
                product["category"],
                product["price"],
                product["cost"],
            ))

        print(f"Inserted {len(products)} products.")

    finally:
        cursor.close()


def insert_orders(connection, orders):
    cursor = connection.cursor()

    try:
        for order in orders:
            cursor.execute("""
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    order_date,
                    status
                )
                VALUES (%s, %s, %s, %s);
            """, (
                order["order_id"],
                order["customer_id"],
                order["order_date"],
                order["status"],
            ))

        print(f"Inserted {len(orders)} orders.")

    finally:
        cursor.close()


def insert_order_items(connection, order_items):
    cursor = connection.cursor()

    try:
        for item in order_items:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
                VALUES (%s, %s, %s, %s);
            """, (
                item["order_id"],
                item["product_id"],
                item["quantity"],
                item["unit_price"],
            ))

        print(f"Inserted {len(order_items)} order items.")

    finally:
        cursor.close()


def filter_valid_orders(orders, order_items, customers):
    valid_customer_ids = {
        int(customer["customer_id"])
        for customer in customers
    }

    valid_orders = [
        order for order in orders
        if int(order["customer_id"]) in valid_customer_ids
    ]

    valid_order_ids = {
        int(order["order_id"])
        for order in valid_orders
    }

    valid_order_items = [
        item for item in order_items
        if int(item["order_id"]) in valid_order_ids
    ]

    rejected_orders = len(orders) - len(valid_orders)
    rejected_items = len(order_items) - len(valid_order_items)

    print(f"Filtered out {rejected_orders} orders referencing rejected customers.")
    print(f"Filtered out {rejected_items} related order items.")

    return valid_orders, valid_order_items


def reset_sequences(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT setval(
                pg_get_serial_sequence('customers', 'customer_id'),
                COALESCE(MAX(customer_id), 1),
                MAX(customer_id) IS NOT NULL
            )
            FROM customers;
        """)

        cursor.execute("""
            SELECT setval(
                pg_get_serial_sequence('products', 'product_id'),
                COALESCE(MAX(product_id), 1),
                MAX(product_id) IS NOT NULL
            )
            FROM products;
        """)

        cursor.execute("""
            SELECT setval(
                pg_get_serial_sequence('orders', 'order_id'),
                COALESCE(MAX(order_id), 1),
                MAX(order_id) IS NOT NULL
            )
            FROM orders;
        """)

        print("PostgreSQL ID sequences reset.")

    finally:
        cursor.close()


def main():
    connection = connect_to_database()

    try:
        customers = load_csv("data/processed/customers_clean.csv")
        products = load_csv("data/generated/products.csv")
        orders = load_csv("data/generated/orders.csv")
        order_items = load_csv("data/generated/order_items.csv")

        orders, order_items = filter_valid_orders(
            orders,
            order_items,
            customers,
        )

        insert_customers(connection, customers)
        insert_products(connection, products)
        insert_orders(connection, orders)
        insert_order_items(connection, order_items)

        reset_sequences(connection)

        connection.commit()

        print("All data successfully loaded.")

    except Exception as error:
        connection.rollback()
        print(f"Loading failed: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
