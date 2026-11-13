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


