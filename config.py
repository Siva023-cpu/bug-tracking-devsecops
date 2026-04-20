import os
import sys

# Base path for normal run and exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create database folder automatically
DB_FOLDER = os.path.join(BASE_DIR, "database")
os.makedirs(DB_FOLDER, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(DB_FOLDER, 'bugtracker.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload paths
    BUG_UPLOAD = os.path.join(BASE_DIR, "app", "static", "bug_attachments")
    SOLUTION_UPLOAD = os.path.join(BASE_DIR, "app", "static", "solution_attachments")

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "txt", "log"}

    # Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")