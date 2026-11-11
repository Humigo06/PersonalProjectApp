import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()



def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL"
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can discover them
    from . import models

    @app.route("/")
    def home():
        return "Project Tracker is running!"

    @app.route("/test-db")
    def test_db():
        from .models import TestEntry

        entry = TestEntry(message="Database connection successful!")
        db.session.add(entry)
        db.session.commit()

        return f"Saved to database: {entry.message}"

    return app