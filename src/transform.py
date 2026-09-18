import csv
import os


INPUT_FILE = "data/raw/customers_dirty.csv"
OUTPUT_FILE = "data/processed/customers_clean.csv"


def load_customers(filepath):
    customers = []

    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customers.append(row)

    return customers


def clean_emails(customers):
    for customer in customers:
        email = customer["email"]

        if email:
            customer["email"] = email.strip().lower()

    return customers


def clean_countries(customers):
    country_mapping = {
        "uk": "UK",
        "united kingdom": "UK",
    }

    for customer in customers:
        country = customer["country"].strip().lower()

        if country in country_mapping:
            customer["country"] = country_mapping[country]

    return customers


def save_customers(customers, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        fieldnames = customers[0].keys()

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(customers)

    print(f"Saved {len(customers)} rows to {filepath}")


def main():
    print("Transforming customer data...")

    customers = load_customers(INPUT_FILE)

    clean_emails(customers)
    clean_countries(customers)

    save_customers(customers, OUTPUT_FILE)

    print("Transformation complete.")


if __name__ == "__main__":
    main()