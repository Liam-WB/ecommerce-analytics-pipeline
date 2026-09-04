import random
import csv

from datetime import date, timedelta

from faker import Faker


fake = Faker()

NUM_CUSTOMERS = 1000
NUM_ORDERS = 10000

COUNTRIES = [
    "UK",
    "USA",
    "Canada",
    "Australia",
    "Germany",
    "France",
    "Spain",
    "Ireland",
]

PRODUCTS = [
    ("Apple", "Fruit", 0.80, 0.40),
    ("Banana", "Fruit", 0.60, 0.30),
    ("Orange", "Fruit", 0.75, 0.35),
    ("Carrot", "Vegetables", 0.50, 0.30),
    ("Potato", "Vegetables", 1.20, 0.50),
    ("Broccoli", "Vegetables", 1.50, 0.70),
    ("Milk", "Dairy", 1.50, 0.90),
    ("Cheese", "Dairy", 3.50, 2.00),
    ("Yoghurt", "Dairy", 1.20, 0.70),
    ("Bread", "Bakery", 1.20, 0.60),
    ("Croissant", "Bakery", 1.80, 0.90),
    ("Chicken Breast", "Meat", 6.50, 4.00),
    ("Beef Mince", "Meat", 5.50, 3.50),
    ("Salmon", "Meat", 8.00, 5.00),
    ("Orange Juice", "Drinks", 2.50, 1.40),
    ("Coffee", "Drinks", 4.50, 2.50),
    ("Tea", "Drinks", 3.00, 1.50),
    ("Chocolate", "Snacks", 1.50, 0.70),
    ("Crisps", "Snacks", 1.20, 0.60),
    ("Biscuits", "Snacks", 1.80, 0.90),
]


def generate_customers(number):
    customers = []

    for _ in range(number):
        customer = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "country": random.choice(COUNTRIES),
            "signup_date": fake.date_between(
                start_date=date(2023, 1, 1),
                end_date=date(2026, 1, 1),
            ),
        }

        customers.append(customer)

    return customers


def generate_products():
    products = []

    for name, category, price, cost in PRODUCTS:
        product = {
            "name": name,
            "category": category,
            "price": price,
            "cost": cost,
        }

        products.append(product)

    return products


def generate_orders(number, customer_count):
    orders = []

    start_date = date(2024, 1, 1)
    end_date = date(2026, 8, 1)

    date_range = (end_date - start_date).days

    for _ in range(number):
        order = {
            "customer_id": random.randint(1, customer_count),
            "order_date": start_date + timedelta(
                days=random.randint(0, date_range)
            ),
            "status": random.choices(
                ["Delivered", "Processing", "Sent", "Cancelled"],
                weights=[70, 10, 15, 5],
            )[0],
        }

        orders.append(order)

    return orders


def generate_order_items(orders, product_count):
    order_items = []

    for order_id in range(1, len(orders) + 1):
        number_of_items = random.randint(1, 5)

        selected_products = random.sample(
            range(1, product_count + 1),
            number_of_items,
        )

        for product_id in selected_products:
            quantity = random.randint(1, 5)

            product = PRODUCTS[product_id - 1]
            unit_price = product[2]

            order_item = {
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
            }

            order_items.append(order_item)

    return order_items


def save_data(customers, products, orders, order_items):
    output_dir = "data/generated"

    import os
    os.makedirs(output_dir, exist_ok=True)

    datasets = {
        "customers.csv": customers,
        "products.csv": products,
        "orders.csv": orders,
        "order_items.csv": order_items,
    }

    for filename, data in datasets.items():
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"Saved {len(data)} rows to {filepath}")


def main():
    print("Generating e-commerce data...")

    customers = generate_customers(NUM_CUSTOMERS)

    products = generate_products()

    orders = generate_orders(
        NUM_ORDERS,
        len(customers),
    )

    order_items = generate_order_items(
        orders,
        len(products),
    )

    save_data(
        customers,
        products,
        orders,
        order_items,
    )

    print("Data generation complete.")


if __name__ == "__main__":
    main()