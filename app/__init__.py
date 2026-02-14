from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Flask-Login Settings
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Import models (IMPORTANT for Flask-Login user_loader)
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.bugs import bugs_bp
    from app.routes.admin import admin_bp
    from app.routes.main import main

    app.register_blueprint(auth_bp)
    app.register_blueprint(bugs_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main)

    # Create DB tables (only for development)
    with app.app_context():
        db.create_all()

    return app
