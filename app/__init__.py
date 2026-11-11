import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL"
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Import models so Flask-Migrate can discover them
    from . import models

    # Register authentication routes
    from . import auth
    app.register_blueprint(auth.auth)

    @app.route("/")
    def home():
        return "Project Tracker is running!"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))


    return app