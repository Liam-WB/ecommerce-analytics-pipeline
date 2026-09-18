```python
import csv
import os


INPUT_FILE = "data/raw/customers_dirty.csv"
OUTPUT_FILE = "data/processed/customers_clean.csv"
REJECTED_FILE = "data/processed/customers_rejected.csv"


CUSTOMER_FIELDS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "country",
    "signup_date",
]

REJECTED_FIELDS = CUSTOMER_FIELDS + ["rejection_reason"]


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


def find_duplicate_emails(customers):
    email_counts = {}

    for customer in customers:
        email = customer["email"]

        if email:
            email_counts[email] = email_counts.get(email, 0) + 1

    duplicate_emails = {
        email
        for email, count in email_counts.items()
        if count > 1
    }

    return duplicate_emails


def validate_customer(customer, duplicate_emails):
    errors = []

    if not customer["email"]:
        errors.append("Missing email")
    elif customer["email"] in duplicate_emails:
        errors.append("Duplicate email")

    if not customer["first_name"]:
        errors.append("Missing first name")

    if not customer["last_name"]:
        errors.append("Missing last name")

    return errors


def separate_valid_and_rejected(customers):
    duplicate_emails = find_duplicate_emails(customers)

    valid_customers = []
    rejected_customers = []

    for customer in customers:
        errors = validate_customer(
            customer,
            duplicate_emails,
        )

        if errors:
            customer["rejection_reason"] = "; ".join(errors)
            rejected_customers.append(customer)
        else:
            valid_customers.append(customer)

    return valid_customers, rejected_customers


def save_customers(customers, filepath, fieldnames):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(customers)

    print(f"Saved {len(customers)} rows to {filepath}")


def print_summary(
    total_customers,
    valid_customers,
    rejected_customers,
):
    print()
    print("Data quality summary")
    print("--------------------")
    print(f"Input rows:      {total_customers}")
    print(f"Valid rows:      {len(valid_customers)}")
    print(f"Rejected rows:   {len(rejected_customers)}")

    if rejected_customers:
        print()
        print("Rejection reasons:")

        reasons = {}

        for customer in rejected_customers:
            reason = customer["rejection_reason"]

            for individual_reason in reason.split("; "):
                reasons[individual_reason] = (
                    reasons.get(individual_reason, 0) + 1
                )

        for reason, count in reasons.items():
            print(f"  {reason}: {count}")


def main():
    print("Transforming customer data...")

    customers = load_customers(INPUT_FILE)

    total_customers = len(customers)

    clean_emails(customers)
    clean_countries(customers)

    valid_customers, rejected_customers = (
        separate_valid_and_rejected(customers)
    )

    save_customers(
        valid_customers,
        OUTPUT_FILE,
        CUSTOMER_FIELDS,
    )

    save_customers(
        rejected_customers,
        REJECTED_FILE,
        REJECTED_FIELDS,
    )

    print_summary(
        total_customers,
        valid_customers,
        rejected_customers,
    )

    print()
    print("Transformation complete.")


if __name__ == "__main__":
    main()
```
