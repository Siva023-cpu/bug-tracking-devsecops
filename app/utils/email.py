from flask_mail import Message
from flask import current_app
from app import mail
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from threading import Thread

# --------------------------
# Token Utilities
# --------------------------
def get_serializer():
    """Return a URLSafeTimedSerializer using app secret key."""
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

def generate_token(email, salt):
    """Generate a signed token for email verification or password reset."""
    serializer = get_serializer()
    return serializer.dumps(email, salt=salt)

def verify_token(token, salt, expiry=3600):
    """Verify token and return email. Returns None if invalid or expired."""
    serializer = get_serializer()
    try:
        return serializer.loads(token, salt=salt, max_age=expiry)
    except (SignatureExpired, BadSignature):
        return None

# --------------------------
# Async Email Sending
# --------------------------
def send_async_email(app, msg):
    """Send email in a separate thread."""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"[Email Error] Could not send email: {e}")

def send_email(to, subject, body, html_body=None):
    """
    Send email asynchronously.
    :param to: Recipient email
    :param subject: Email subject
    :param body: Plain text body
    :param html_body: Optional HTML body
    """
    if not current_app.config.get("MAIL_USERNAME"):
        print("[Email Warning] Mail not configured.")
        return

    msg = Message(subject, recipients=[to])
    msg.body = body
    if html_body:
        msg.html = html_body

    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
