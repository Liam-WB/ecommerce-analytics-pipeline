import csv
import random


INPUT_FILE = "data/generated/customers.csv"
OUTPUT_FILE = "data/raw/customers_dirty.csv"


def load_customers(filepath):
    customers = []

    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customers.append(row)

    return customers


def add_whitespace(customers, percentage=0.05):
    number_to_modify = int(len(customers) * percentage)

    selected_customers = random.sample(customers, number_to_modify)

    for customer in selected_customers:
        customer["email"] = f"  {customer['email']}  "

    return customers


def change_country_case(customers, percentage=0.05):
    number_to_modify = int(len(customers) * percentage)

    selected_customers = random.sample(customers, number_to_modify)

    for customer in selected_customers:
        customer["country"] = customer["country"].lower()

    return customers


def remove_emails(customers, percentage=0.02):
    number_to_modify = int(len(customers) * percentage)

    selected_customers = random.sample(customers, number_to_modify)

    for customer in selected_customers:
        customer["email"] = ""

    return customers


def duplicate_emails(customers, percentage=0.01):
    number_to_modify = int(len(customers) * percentage)

    selected_customers = random.sample(customers, number_to_modify)

    for customer in selected_customers:
        other_customer = random.choice(customers)

        customer["email"] = other_customer["email"]

    return customers


def change_country_name(customers, percentage=0.02):
    number_to_modify = int(len(customers) * percentage)

    selected_customers = random.sample(customers, number_to_modify)

    for customer in selected_customers:
        if customer["country"] == "UK":
            customer["country"] = "United Kingdom"

    return customers


def save_customers(customers, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        fieldnames = customers[0].keys()

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(customers)

    print(f"Saved {len(customers)} customers to {filepath}")


def main():
    print("Creating dirty customer data...")

    customers = load_customers(INPUT_FILE)

    add_whitespace(customers)
    change_country_case(customers)
    remove_emails(customers)
    duplicate_emails(customers)
    change_country_name(customers)

    save_customers(customers, OUTPUT_FILE)

    print("Dirty data generation complete.")


if __name__ == "__main__":
    main()