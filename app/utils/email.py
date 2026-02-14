from flask_mail import Message
from flask import current_app
from app import mail
from itsdangerous import URLSafeTimedSerializer

def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

def generate_token(email, salt):
    serializer = get_serializer()
    return serializer.dumps(email, salt=salt)

def verify_token(token, salt, expiry=3600):
    serializer = get_serializer()
    return serializer.loads(token, salt=salt, max_age=expiry)

def send_email(to, subject, body):
    if not current_app.config.get("MAIL_USERNAME"):
        print("Mail not configured")
        return

    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)
