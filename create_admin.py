
import sqlite3
from werkzeug.security import generate_password_hash
from getpass import getpass

name = input("Enter Admin Name: ")
email = input("Enter Admin Email: ")
password = getpass("Enter Admin Password: ")
phone = input("Enter Admin Phone: ")

hashed_password = generate_password_hash(password)

connection = sqlite3.connect("food_waste.db")
cursor = connection.cursor()

try:
    cursor.execute("""
        INSERT INTO users
        (full_name, email, password, phone, role)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, hashed_password, phone, "Admin"))

    connection.commit()
    print("Admin account created successfully!")

except sqlite3.IntegrityError:
    print("This email is already registered!")

finally:
    connection.close()
