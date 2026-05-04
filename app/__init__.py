from flask import Flask
from dotenv import load_dotenv
import os

from .extensions import db, login_manager, mail, migrate


def create_app():

    load_dotenv()

    app = Flask(__name__)

    # ======================
    # CONFIG
    # ======================
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = False

    # ======================
    # DATABASE (RAILWAY SAFE FIX)
    # ======================
    database_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")

    if not database_url:
        raise Exception("DATABASE_URL is missing in Railway environment variables")

    # Fix Railway postgres format issue
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"}
    }

    # ======================
    # MAIL CONFIG
    # ======================
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # ======================
    # INIT EXTENSIONS
    # ======================
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # ======================
    # MODELS
    # ======================
    from app.models.user import User
    from app.models.receipt import Receipt
    from app.models.company import Company

    # ======================
    # USER LOADER
    # ======================
    @login_manager.user_loader
    def load_user(user_id):
        if not user_id:
            return None
        try:
            return db.session.get(User, int(user_id))
        except:
            return None

    # ======================
    # BLUEPRINTS
    # ======================
    from .routes.receipt_routes import receipt_bp
    app.register_blueprint(receipt_bp, url_prefix="/receipt")

    try:
        from .routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp)
    except:
        pass

    return app