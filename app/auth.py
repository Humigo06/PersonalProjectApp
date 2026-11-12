from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from . import db
from .models import User, Collection, Project


auth = Blueprint("auth",__name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Basic input validation
        if not username or not email or not password:
            flask("Please fill out all fields.", "error")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters." "error")
            return redirect(url_for("auth.register"))

        # Create the new user
        user = User(username=username, email=email)
        user.set_password(password)

        # Create their default collection
        default_collection = Collection(
            name="General",
            is_default=True,
            user=user
        )

        db.session.add(user)
        db.session.add(default_collection)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("That username or email is already in use.", "error")
            return redirect(url_for("auth.register"))

        # Log in the newly registed user
        login_user(user)

        flash("Your account was created successfully!", "success")

        return redirect(url_for("auth.library"))

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash("Invalid username or password.", "error")
            return redirect(url_for("auth.login"))

        login_user(user)

        return redirect(url_for("auth.library"))

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))

@auth.route("/library")
@login_required
def library():
    projects = Project.query.filter_by(
        user_id=current_user.id
    ).all()

    collections = Collection.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "library.html",
        projects=projects,
        collections=collections
    )