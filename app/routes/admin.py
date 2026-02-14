from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("Admin access required", "danger")
        return redirect(url_for("bugs.dashboard"))

    # 🔹 Handle Role Update (POST)
    if request.method == "POST":
        user = User.query.get(int(request.form["user_id"]))
        user.role = request.form["role"]
        db.session.commit()
        flash("Role updated", "success")
        return redirect(url_for("admin.manage_users"))

    # 🔹 Handle Search + Pagination (GET)
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()

    query = User.query

    # Apply search filter
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    pagination = query.order_by(User.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    users = pagination.items

    return render_template(
        "admin/admin_users.html",
        users=users,
        pagination=pagination,
        search=search
    )


@admin_bp.route("/admin/users/add", methods=["GET", "POST"])
@login_required
def add_user():
    if current_user.role != "admin":
        flash("Admin access required", "danger")
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # Hash the password
        password_hash = generate_password_hash(password)

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            is_verified=False  # optional
        )

        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully", "success")
        return redirect(url_for("admin.manage_users"))

    return render_template("admin/add_user.html")


@admin_bp.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        flash("Admin access required", "danger")
        return redirect(url_for("bugs.dashboard"))

    user = User.query.get_or_404(user_id)

    # Optional: Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash("You cannot delete your own account!", "warning")
        return redirect(url_for("admin.manage_users"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' has been deleted.", "success")
    return redirect(url_for("admin.manage_users"))

@admin_bp.route("/admin/users/<int:user_id>")
@login_required
def view_user(user_id):
    if current_user.role != "admin":
        flash("Admin access required", "danger")
        return redirect(url_for("main.dashboard"))

    user = User.query.get_or_404(user_id)
    return render_template("admin/user_profile.html", user=user)
