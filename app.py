from flask import Flask, render_template, request, redirect, url_for, session, flash
import  os
from werkzeug.security import check_password_hash
from database import (
    add_food_listing,
    get_all_food_listings,
    search_food_by_area,
    register_user,
    get_user_by_email,
    get_donor_food_listings,
    update_food_listing,
    get_food_listing_by_id,
    delete_food_listing,
    get_available_food_listings,
    create_donation_request,
    get_donor_requests,
    update_request_status,
    get_receiver_requests,
    complete_donation_request,
    get_all_users,
get_all_donations,
get_all_requests,
delete_user
)
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/about")
def about():
    return "About Food Waste Rescue - Reducing food waste, helping people!"
@app.route("/donate", methods=["GET", "POST"])
@app.route("/donate", methods=["GET", "POST"])
def donate():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Donor":
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        food_name = request.form.get("food_name")
        quantity = request.form.get("quantity")
        location = request.form.get("location")
        expiry_time = request.form.get("expiry_time")

        user_id = session["user_id"]

        add_food_listing(
            food_name,
            quantity,
            location,
            expiry_time,
            user_id
        )

        flash("Food donation added successfully!")

        return redirect(url_for("dashboard"))

    return render_template("donate.html")
@app.route("/search")
def search():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Receiver":
        return "Access denied!"

    area = request.args.get("area", "").strip()

    if not area:
        return redirect(url_for("dashboard"))

    food_listings = search_food_by_area(area)

    return render_template(
        "receiver_dashboard.html",
        food_listings=food_listings
    )
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        role = request.form.get("role")

        register_user(full_name, email, password, phone, role)

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_role"] = user[5]

            if user[5] == "Admin":
                return redirect(url_for("admin_dashboard"))

            else:
                return redirect(url_for("dashboard"))

        else:
            flash("Invalid email or password!")

    return render_template("login.html")

@app.route("/dashboard")
@app.route("/dashboard")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session["user_role"]

    if role == "Donor":

        food_listings = get_donor_food_listings(
            session["user_id"]
        )

        donor_requests = get_donor_requests(
            session["user_id"]
        )

        return render_template(
            "donor_dashboard.html",
            food_listings=food_listings,
            donor_requests=donor_requests
        )

    elif role == "Receiver":

        food_listings = get_available_food_listings()

        receiver_requests = get_receiver_requests(
            session["user_id"]
        )

        return render_template(
            "receiver_dashboard.html",
            food_listings=food_listings,
            receiver_requests=receiver_requests
        )

    elif role == "Admin":
        return redirect(url_for("admin_dashboard"))

    else:
        return "Invalid user role!"


@app.route("/edit-food/<int:food_id>", methods=["GET", "POST"])
def edit_food(food_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Donor":
        return "Access denied!"

    user_id = session["user_id"]

    if request.method == "POST":

        food_name = request.form.get("food_name")
        quantity = request.form.get("quantity")
        location = request.form.get("location")
        expiry_time = request.form.get("expiry_time")

        updated = update_food_listing(
            food_id, food_name, quantity,
            location, expiry_time, user_id
        )

        if updated == 0:
            return "Donation not found or access denied!"

        return redirect(url_for("dashboard"))

    food = get_food_listing_by_id(food_id, user_id)

    if food is None:
        return "Donation not found or access denied!"

    return render_template("edit_food.html", food=food)
@app.route("/delete-food/<int:food_id>", methods=["POST"])
def delete_food(food_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Donor":
        return "Access denied!"

    deleted = delete_food_listing(
        food_id,
        session["user_id"]
    )

    if deleted == 0:
        return "Donation not found or access denied!"

    return redirect(url_for("dashboard"))
@app.route("/request-food/<int:listing_id>", methods=["POST"])
def request_food(listing_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Receiver":
        return "Only receivers can request food!"

    receiver_id = session["user_id"]

    success = create_donation_request(listing_id, receiver_id)

    if success:
        flash("Food request submitted successfully!")
    else:
        flash("You already have a pending request for this food!")

    return redirect(url_for("dashboard"))

@app.route("/update-request/<int:request_id>/<status>", methods=["POST"])
def update_request(request_id, status):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Donor":
        return "Access denied!"

    if status not in ["Accepted", "Rejected"]:
        return "Invalid status!"

    updated = update_request_status(
        request_id,
        session["user_id"],
        status
    )

    if updated:
        flash(f"Request {status.lower()} successfully!")
    else:
        flash("Request not found or already processed.")

    return redirect(url_for("dashboard"))


@app.route("/complete-request/<int:request_id>", methods=["POST"])
def complete_request(request_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Receiver":
        return "Access denied!"

    updated = complete_donation_request(
        request_id,
        session["user_id"]
    )

    if updated:
        flash("Food collection marked as completed!")
    else:
        flash("Request not found or not yet accepted.")

    return redirect(url_for("dashboard"))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin-dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Admin":
        return redirect(url_for("dashboard"))

    users = get_all_users()
    donations = get_all_donations()
    requests_data = get_all_requests()

    return render_template(
        "admin_dashboard.html",
        users=users,
        donations=donations,
        requests_data=requests_data
    )
@app.route("/admin/delete-user/<int:user_id>", methods=["POST"])
def admin_delete_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"] != "Admin":
        return "Access denied!"

    deleted = delete_user(user_id)

    if deleted:
        flash("User account deleted successfully!")
    else:
        flash("User not found or cannot be deleted!")

    return redirect(url_for("admin_dashboard"))
@app.route("/foods")
def foods():
    food_listings = get_available_food_listings()
    return render_template("foods.html", food_listings=food_listings)
if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
