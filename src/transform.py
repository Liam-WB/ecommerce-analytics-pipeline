
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


# Accepted countries and their standardised names
COUNTRY_MAPPING = {
    "uk": "UK",
    "united kingdom": "UK",
    "usa": "USA",
    "canada": "Canada",
    "australia": "Australia",
    "germany": "Germany",
    "france": "France",
    "spain": "Spain",
    "ireland": "Ireland",
}

VALID_COUNTRIES = set(COUNTRY_MAPPING.values())


def load_customers(filepath):
    customers = []

    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customers.append(row)

    return customers


def clean_emails(customers):
    for customer in customers:
        email = customer.get("email", "")

        customer["email"] = email.strip().lower() if email else ""

    return customers


def clean_names(customers):
    for customer in customers:
        customer["first_name"] = customer.get("first_name", "").strip()
        customer["last_name"] = customer.get("last_name", "").strip()

    return customers


def clean_countries(customers):
    for customer in customers:
        country = customer.get("country", "").strip().lower()

        if country in COUNTRY_MAPPING:
            customer["country"] = COUNTRY_MAPPING[country]
        else:
            customer["country"] = country

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

    email = customer["email"]
    first_name = customer["first_name"]
    last_name = customer["last_name"]
    country = customer["country"]

    if not email:
        errors.append("Missing email")
    elif email in duplicate_emails:
        errors.append("Duplicate email")

    if not first_name:
        errors.append("Missing first name")

    if not last_name:
        errors.append("Missing last name")

    if not country:
        errors.append("Missing country")
    elif country not in VALID_COUNTRIES:
        errors.append("Unrecognised country")

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
            rejected_customer = customer.copy()
            rejected_customer["rejection_reason"] = "; ".join(errors)

            rejected_customers.append(rejected_customer)
        else:
            valid_customers.append(customer)

    return valid_customers, rejected_customers


def save_customers(customers, filepath, fieldnames):
    directory = os.path.dirname(filepath)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(customers)

    print(f"Saved {len(customers)} rows to {filepath}")


def print_summary(
    total_customers,
    valid_customers,
    rejected_customers,
):
    valid_count = len(valid_customers)
    rejected_count = len(rejected_customers)

    if total_customers:
        valid_percentage = (valid_count / total_customers) * 100
        rejected_percentage = (rejected_count / total_customers) * 100
    else:
        valid_percentage = 0
        rejected_percentage = 0

    print()
    print("Data quality summary")
    print("--------------------")
    print(f"Input rows:       {total_customers}")
    print(f"Valid rows:       {valid_count} ({valid_percentage:.1f}%)")
    print(f"Rejected rows:    {rejected_count} ({rejected_percentage:.1f}%)")

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

    try:
        customers = load_customers(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: Input file not found: {INPUT_FILE}")
        return

    total_customers = len(customers)

    clean_emails(customers)
    clean_names(customers)
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
