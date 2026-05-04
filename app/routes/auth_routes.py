from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from app.models.user import User

auth_bp = Blueprint("auth", __name__)


# ======================
# LOGIN ROUTE
# ======================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        print("USER:", user)

        if user and user.password == password:
            login_user(user)

            return redirect(url_for("receipt.dashboard"))

        return "Invalid credentials", 401

    return render_template("login.html")
# ======================
# LOGOUT ROUTE
# ======================
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))