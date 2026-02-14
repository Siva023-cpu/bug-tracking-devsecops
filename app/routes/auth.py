from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db, login_manager
from app.utils.email import generate_token, verify_token, send_email

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("auth.register"))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("auth.login"))

        # Determine role (first user is admin)
        role = "admin" if not User.query.first() else "user"

        user = User(username=username, email=email,
                    password_hash=password, role=role)

        db.session.add(user)
        db.session.commit()

        # Generate verification token
        token = generate_token(email, "verify")
        link = url_for("auth.verify_email", token=token, _external=True)

        send_email(email, "Verify Account",
                   f"Click to verify:\n\n{link}")

        flash("Check your email to verify account", "info")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"]
        ).first()

        if not user or not check_password_hash(
                user.password_hash,
                request.form["password"]):
            flash("Invalid credentials", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_verified:
            flash("Verify email first", "warning")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/verify/<token>")
def verify_email(token):
    try:
        email = verify_token(token, "verify")
        user = User.query.filter_by(email=email).first()
        user.is_verified = True
        db.session.commit()
        flash("Email verified", "success")
    except:
        flash("Invalid/Expired link", "danger")

    return redirect(url_for("auth.login"))

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found", "danger")
            return redirect(url_for("auth.forgot_password"))

        # Generate a password reset token
        token = generate_token(email, "reset")
        link = url_for("auth.reset_password", token=token, _external=True)

        # Send reset link via email
        send_email(email, "Password Reset Request",
                   f"Click the link below to reset your password:\n\n{link}")

        flash("Password reset link sent to your email", "info")
        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")



@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(current_user.password_hash, current_password):
            flash("Current password is incorrect", "danger")
        elif new_password != confirm_password:
            flash("New passwords do not match", "danger")
        else:
            current_user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash("Password updated successfully!", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("change_password.html")

@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = verify_token(token, "reset")
    except:
        flash("Invalid or expired reset link", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match", "danger")
        else:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash("Password reset successful! Please login.", "success")
            return redirect(url_for("auth.login"))

    return render_template("reset_password.html")

@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@auth_bp.route("/edit-profile", methods=["POST"])
@login_required
def edit_profile():
    user = current_user
    username = request.form.get("username")
    email = request.form.get("email")

    # Optional: check if new username/email already exists
    if User.query.filter(User.username==username, User.id!=user.id).first():
        flash("Username already taken", "danger")
        return redirect(url_for("auth.profile"))

    if User.query.filter(User.email==email, User.id!=user.id).first():
        flash("Email already in use", "danger")
        return redirect(url_for("auth.profile"))

    user.username = username
    user.email = email
    db.session.commit()
    flash("Profile updated successfully!", "success")
    return redirect(url_for("auth.profile"))
