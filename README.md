# Food Waste Rescue

## Project Overview
Food Waste Rescue is a web-based application developed using Python Flask to reduce food waste by connecting food donors with NGOs and charitable organizations.

The application allows donors to share surplus food, while receivers can browse available food and request donations.

## Features
- User registration and login
- Role-based access for Donors, Receivers and Admin
- Secure password hashing
- Add, edit and delete food donations
- Search food donations by Hyderabad location
- Request and manage food donations
- Track donation request status
- Admin dashboard to manage users, donations and requests
- Admin account deletion with protection for Admin accounts

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2
- Werkzeug

## User Roles
1. **Donor:** Adds and manages surplus food donations.
2. **Receiver:** Browses available food and requests donations.
3. **Admin:** Views and manages users, food donations and donation requests.

## Project Location
The application is designed for Hyderabad, Telangana, India.

## How to Run

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install Flask:

   `pip install flask`

4. Run the application:

   `python app.py`

5. Open your browser and visit:

   `http://127.0.0.1:5000`

## Database
SQLite is used to store user accounts, food listings and donation requests.

## Project Purpose
This project was developed to practice Python backend development, database operations, authentication, CRUD operations and role-based access control.
