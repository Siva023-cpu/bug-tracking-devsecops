from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Bug, Notification
from app import db

main = Blueprint("main", __name__)

# -----------------------------
# Home Route
# -----------------------------
@main.route("/")
def home():
    return render_template("home.html")


# -----------------------------
# Dashboard
# -----------------------------
@main.route("/dashboard")
@login_required
def dashboard():
    from app.models import Bug
    from flask import request

    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "all")  # NEW: get status from query params

    # Base query
    query = Bug.query

    # Filter by status if not "all"
    if status_filter != "all":
        query = query.filter_by(status=status_filter)

    # Filter by search input
    if search_query:
        query = query.filter(Bug.title.ilike(f"%{search_query}%"))

    # Order by newest first and paginate
    pagination = query.order_by(Bug.created_at.desc()).paginate(page=page, per_page=5)
    bugs = pagination.items

    # Stats (for cards)
    total_bugs = Bug.query.count()
    open_bugs = Bug.query.filter_by(status="Open").count()
    resolved_bugs = Bug.query.filter_by(status="Resolved").count()

    return render_template(
        "dashboard.html",
        bugs=bugs,
        pagination=pagination,
        total_bugs=total_bugs,
        open_bugs=open_bugs,
        resolved_bugs=resolved_bugs,
        search=search_query,
        status_filter=status_filter  # pass filter to template
    )

# -----------------------------
# Notifications
# -----------------------------
@main.route("/notifications")
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).all()

    return render_template(
        "notifications.html",
        notifications=user_notifications
    )


@main.route("/about")
def about():
    return render_template("about.html")
