from werkzeug.security import generate_password_hash, check_password_hash


import sqlite3

connection = sqlite3.connect("food_waste.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS food_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    location TEXT NOT NULL,
    expiry_time TEXT NOT NULL
)
""")

connection.commit()

print("Food listings table created successfully!")

connection.close()

def add_food_listing(food_name, quantity, location, expiry_time, user_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO food_listings
        (food_name, quantity, location, expiry_time, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (food_name, quantity, location, expiry_time, user_id))

    connection.commit()
    connection.close()

    print("Food listing added successfully!")
def view_food_listings():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM food_listings")

    records = cursor.fetchall()

    for record in records:
        print(record)

    connection.close()
view_food_listings()
def get_all_food_listings():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM food_listings")

    records = cursor.fetchall()

    connection.close()

    return records
def search_food_by_area(area):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM food_listings WHERE location LIKE ?",
        ('%' + area + '%',)
    )

    records = cursor.fetchall()

    connection.close()

    return records
def create_users_table():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Users table created successfully!")
create_users_table()
def register_user(full_name, email, password, phone, role):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("""
            INSERT INTO users
            (full_name, email, password, phone, role)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, email, hashed_password, phone, role))

        connection.commit()
        print("User registered successfully!")

    except sqlite3.IntegrityError:
        print("This email is already registered!")

    finally:
        connection.close()
def get_user_by_email(email):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user
register_user(
    "ABC Restaurant",
    "abc2@gmail.com",
    "test123",
    "9876543210",
    "Donor"
)
def create_food_table():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL,
            expiry_time TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Food table created successfully!")
def add_user_id_column():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(food_listings)")
    columns = [column[1] for column in cursor.fetchall()]

    if "user_id" not in columns:

        cursor.execute("""
            ALTER TABLE food_listings
            ADD COLUMN user_id INTEGER REFERENCES users(user_id)
        """)

        connection.commit()
        print("user_id column added successfully!")

    else:
        print("user_id column already exists!")

    connection.close()
def get_donor_food_listings(user_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM food_listings
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    food_listings = cursor.fetchall()

    connection.close()

    return food_listings
def update_food_listing(food_id, food_name, quantity, location, expiry_time, user_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE food_listings
        SET food_name = ?,
            quantity = ?,
            location = ?,
            expiry_time = ?
        WHERE id = ? AND user_id = ?
    """, (food_name, quantity, location, expiry_time, food_id, user_id))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated
def get_food_listing_by_id(food_id, user_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM food_listings
        WHERE id = ? AND user_id = ?
    """, (food_id, user_id))

    food = cursor.fetchone()

    connection.close()

    return food
def delete_food_listing(food_id, user_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM food_listings
        WHERE id = ? AND user_id = ?
    """, (food_id, user_id))

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted
def get_available_food_listings():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM food_listings
        ORDER BY id DESC
    """)

    food_listings = cursor.fetchall()

    connection.close()

    return food_listings
def create_requests_table():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donation_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (listing_id) REFERENCES food_listings(id),
            FOREIGN KEY (receiver_id) REFERENCES users(user_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Donation requests table created successfully!")
def create_donation_request(listing_id, receiver_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO donation_requests
        (listing_id, receiver_id)
        VALUES (?, ?)
    """, (listing_id, receiver_id))

    connection.commit()
    connection.close()

    print("Donation request submitted successfully!")
def create_donation_request(listing_id, receiver_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    # Check whether this receiver already has a pending request
    cursor.execute("""
        SELECT request_id
        FROM donation_requests
        WHERE listing_id = ? AND receiver_id = ?
        AND status = 'Pending'
    """, (listing_id, receiver_id))

    existing_request = cursor.fetchone()

    if existing_request:
        connection.close()
        return False

    cursor.execute("""
        INSERT INTO donation_requests
        (listing_id, receiver_id)
        VALUES (?, ?)
    """, (listing_id, receiver_id))

    connection.commit()
    connection.close()

    return True
def get_donor_requests(donor_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            donation_requests.request_id,
            food_listings.food_name,
            food_listings.quantity,
            food_listings.location,
            users.full_name,
            donation_requests.status,
            donation_requests.request_date

        FROM donation_requests

        JOIN food_listings
        ON donation_requests.listing_id = food_listings.id

        JOIN users
        ON donation_requests.receiver_id = users.user_id

        WHERE food_listings.user_id = ?
    """, (donor_id,))

    requests = cursor.fetchall()

    connection.close()

    return requests
def update_request_status(request_id, donor_id, new_status):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE donation_requests
        SET status = ?
        WHERE request_id = ?
        AND status = 'Pending'
        AND listing_id IN (
            SELECT id FROM food_listings
            WHERE user_id = ?
        )
    """, (new_status, request_id, donor_id))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated
def get_receiver_requests(receiver_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            donation_requests.request_id,
            food_listings.food_name,
            food_listings.quantity,
            food_listings.location,
            users.full_name,
            donation_requests.status,
            donation_requests.request_date

        FROM donation_requests

        JOIN food_listings
        ON donation_requests.listing_id = food_listings.id

        JOIN users
        ON food_listings.user_id = users.user_id

        WHERE donation_requests.receiver_id = ?
    """, (receiver_id,))

    requests = cursor.fetchall()

    connection.close()

    return requests
def complete_donation_request(request_id, receiver_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE donation_requests
        SET status = 'Completed'
        WHERE request_id = ?
        AND receiver_id = ?
        AND status = 'Accepted'
    """, (request_id, receiver_id))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated

def get_all_users():

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_id, full_name, email, phone, role
        FROM users
        ORDER BY user_id DESC
    """)

    users = cursor.fetchall()

    connection.close()

    return users
def get_all_donations():
    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT food_listings.id,
               food_listings.food_name,
               food_listings.quantity,
               food_listings.location,
               food_listings.expiry_time,
               users.full_name
        FROM food_listings
        LEFT JOIN users
        ON food_listings.user_id = users.user_id
        ORDER BY food_listings.id DESC
    """)

    donations = cursor.fetchall()
    connection.close()

    return donations
def get_all_requests():
    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            donation_requests.request_id,
            food_listings.food_name,
            receiver.full_name,
            donor.full_name,
            donation_requests.status,
            donation_requests.request_date
        FROM donation_requests
        JOIN food_listings
            ON donation_requests.listing_id = food_listings.id
        JOIN users AS receiver
            ON donation_requests.receiver_id = receiver.user_id
        LEFT JOIN users AS donor
            ON food_listings.user_id = donor.user_id
        ORDER BY donation_requests.request_id DESC
    """)

    requests = cursor.fetchall()
    connection.close()

    return requests
def delete_user(user_id):

    connection = sqlite3.connect("food_waste.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None or user[0] == "Admin":
        connection.close()
        return False

    # Delete receiver requests
    cursor.execute("""
        DELETE FROM donation_requests
        WHERE receiver_id = ?
    """, (user_id,))

    # Delete requests associated with donor's donations
    cursor.execute("""
        DELETE FROM donation_requests
        WHERE listing_id IN (
            SELECT id FROM food_listings
            WHERE user_id = ?
        )
    """, (user_id,))

    # Delete donor's food listings
    cursor.execute("""
        DELETE FROM food_listings
        WHERE user_id = ?
    """, (user_id,))

    # Delete user account
    cursor.execute(
        "DELETE FROM users WHERE user_id = ?",
        (user_id,)
    )

    connection.commit()
    connection.close()

    return True