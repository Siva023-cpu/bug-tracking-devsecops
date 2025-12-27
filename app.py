from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os

from models import db, User, Bug, Solution, Notification

# ---------------- APP CONFIG ---------------- #

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "bugtracker.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

BUG_UPLOAD = os.path.join(BASE_DIR, "uploads", "bug_attachments")
SOLUTION_UPLOAD = os.path.join(BASE_DIR, "uploads", "solution_attachments")

app.config["BUG_UPLOAD"] = BUG_UPLOAD
app.config["SOLUTION_UPLOAD"] = SOLUTION_UPLOAD

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "txt", "log"}

db.init_app(app)

print("🔥 DATABASE:", app.config["SQLALCHEMY_DATABASE_URI"])

# ---------------- HELPERS ---------------- #

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required():
    user = get_current_user()
    return user and user.role == "admin"


def get_current_user():
    if "user" not in session:
        return None
    return User.query.filter_by(username=session["user"]).first()


@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())



# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return redirect(url_for("dashboard")) if "user" in session else render_template("home.html")


# -------- AUTH -------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        # ✅ FIRST USER = ADMIN (RELIABLE)
        role = "admin" if not User.query.first() else "user"

        user = User(
            username=username,
            email=email,
            password=password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))

        session.clear()
        session["user"] = user.username
        session["role"] = user.role
        session["is_admin"] = True if user.role == "admin" else False  # ✅ FIX

        return redirect(url_for("dashboard"))

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


# -------- DASHBOARD -------- #

@app.route("/dashboard")
@login_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Bug.query
    if search:
        query = query.filter(Bug.title.ilike(f"%{search}%"))

    pagination = query.order_by(Bug.id.desc()).paginate(page=page, per_page=5, error_out=False)

    return render_template(
        "dashboard.html",
        bugs=pagination.items,
        pagination=pagination,
        total=Bug.query.count(),
        open_bugs=Bug.query.filter(Bug.status != "Resolved").count(),
        resolved=Bug.query.filter(Bug.status == "Resolved").count(),
        search=search
    )

@app.route("/bug/<int:bug_id>/update-status", methods=["POST"])
@login_required
def update_status(bug_id):
    if session.get("role") != "admin":
        flash("Admin access required", "danger")
        return redirect(url_for("dashboard"))

    bug = Bug.query.get_or_404(bug_id)
    new_status = request.form.get("status")

    if new_status:
        bug.status = new_status
        db.session.commit()
        flash("Bug status updated", "success")

    return redirect(url_for("dashboard", updated=bug_id))



# -------- ADD BUG -------- #

@app.route("/add-bug", methods=["GET", "POST"])
@login_required
def add_bug():
    if request.method == "POST":
        file = request.files.get("attachment")
        filename = None

        if file and allowed_file(file.filename):
            os.makedirs(app.config["BUG_UPLOAD"], exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["BUG_UPLOAD"], filename))

        bug = Bug(
            title=request.form["title"],
            description=request.form["description"],
            severity=request.form["severity"],
            reported_by=session["user"],
            attachment=filename
        )

        db.session.add(bug)
        db.session.commit()

        flash("Bug reported successfully", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_bug.html")


# -------- BUG DETAILS -------- #

@app.route("/bug/<int:bug_id>", methods=["GET", "POST"])
@login_required
def bug_detail(bug_id):
    bug = Bug.query.get_or_404(bug_id)

    if request.method == "POST":
        file = request.files.get("solution_attachment")
        filename = None

        if file and allowed_file(file.filename):
            os.makedirs(app.config["SOLUTION_UPLOAD"], exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["SOLUTION_UPLOAD"], filename))

        solution = Solution(
            content=request.form["solution"],
            attachment=filename,
            bug_id=bug.id,
            user=session["user"]
        )

        bug.status = "Resolved"

        db.session.add(solution)
        db.session.add(Notification(
            message=f"Your bug '{bug.title}' has been resolved",
            user=bug.reported_by
        ))

        db.session.commit()
        flash("Solution submitted successfully", "success")

    return render_template("bug_detail.html", bug=bug)


# -------- ADMIN USERS -------- #

@app.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():
    if session.get("role") != "admin":
        flash("Admin access required", "danger")
        return redirect(url_for("dashboard"))

    users = User.query.all()

    if request.method == "POST":
        user_id = request.form["user_id"]
        role = request.form["role"]

        user = User.query.get(int(user_id))
        user.role = role
        db.session.commit()

        # ✅ UPDATE SESSION IF CURRENT USER ROLE CHANGED
        if user.username == session.get("user"):
            session["role"] = role
            session["is_admin"] = True if role == "admin" else False

        flash("User role updated", "success")
        return redirect(url_for("manage_users"))

    return render_template("admin_users.html", users=users)


    return render_template("admin_users.html", users=User.query.all())
# -------- NOTIFICATIONS -------- #

@app.route("/notifications")
@login_required
def notifications():
    notes = Notification.query.filter_by(user=session["user"]).order_by(Notification.created_at.desc())
    return render_template("notifications.html", notifications=notes)


# -------- FILE DOWNLOADS -------- #

@app.route("/bug-uploads/<filename>")
@login_required
def bug_upload(filename):
    return send_from_directory(app.config["BUG_UPLOAD"], filename)

@app.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(
        app.config["BUG_UPLOAD"],
        filename
    )
@app.route("/solution-uploads/<filename>")
@login_required
def solution_upload(filename):
    return send_from_directory(app.config["SOLUTION_UPLOAD"], filename)

@app.route("/download/solution/<filename>")
@login_required
def download_solution(filename):
    return send_from_directory(
        app.config["SOLUTION_UPLOAD"],
        filename,
        as_attachment=True
    )



# ---------------- START ---------------- #

with app.app_context():
    db.create_all()

    # ✅ SAFETY: Ensure at least one admin
    if not User.query.filter_by(role="admin").first():
        first_user = User.query.first()
        if first_user:
            first_user.role = "admin"
            db.session.commit()
            print("⚡ Auto-promoted admin:", first_user.username)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
