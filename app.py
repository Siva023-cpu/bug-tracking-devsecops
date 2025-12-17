from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Bug, Comment   # ✅ use Comment consistently
from functools import wraps
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL# DATABASE CHANGE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------- LOGIN REQUIRED DECORATOR ----------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
# ---------- HOME ----------
@app.route('/')
def home():
    if 'user' in session:                      # ✅ FIX auto-login confusion
        return redirect(url_for('dashboard'))
    return render_template('home.html')

# ---------- AUTH ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for('register'))

        is_admin = User.query.count() == 0

        user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('User not registered. Please register first.', 'danger')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password.', 'danger')
            return redirect(url_for('login'))

        session.clear()
        session['user'] = user.username
        session['is_admin'] = user.is_admin

        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()  
    flash("You have been logged out successfully.", "info")                         # ✅ FIX
    return redirect(url_for('login'))

# ---------- DASHBOARD ----------
@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Bug.query

    if search:
        query = query.filter(Bug.title.ilike(f"%{search}%"))

    pagination = query.order_by(Bug.id.desc()).paginate(page=page, per_page=5)

    bugs = pagination.items

    total = Bug.query.count()
    open_bugs = Bug.query.filter(Bug.status != 'Resolved').count()
    resolved = Bug.query.filter(Bug.status == 'Resolved').count()

    return render_template(
        'dashboard.html',
        bugs=bugs,
        pagination=pagination,
        total=total,
        open_bugs=open_bugs,
        resolved=resolved,
        search=search
    )

# ---------- ADD BUG ----------
@app.route('/add-bug', methods=['GET', 'POST'])
@login_required
def add_bug():
    if request.method == 'POST':
        bug = Bug(
            title=request.form['title'],
            description=request.form['description'],
            severity=request.form['severity'],
            reported_by=session['user']
        )
        db.session.add(bug)
        db.session.commit()

        flash("Bug reported successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_bug.html')

# ---------- UPDATE STATUS ----------
@app.route('/update-status/<int:bug_id>', methods=['POST'])
@login_required
def update_status(bug_id):
    if not session.get('is_admin'):
        flash("Admin access required", "danger")
        return redirect(url_for('dashboard'))

    bug = Bug.query.get_or_404(bug_id)
    bug.status = request.form['status']
    db.session.commit()

    flash("Bug status updated", "success")
    return redirect(url_for('dashboard',updated=bug.id))

# ---------- BUG DETAILS & COMMENTS ----------
@app.route('/bug/<int:bug_id>', methods=['GET', 'POST'])
@login_required
def bug_detail(bug_id):
    bug = Bug.query.get_or_404(bug_id)

    if request.method == 'POST':
        comment = Comment(
            content=request.form['solution'],
            bug_id=bug.id,
            user=session['user']              # ✅ FIXED
        )
        if bug.status != "Resolved":
            bug.status = "Resolved"
      #  status when solution added
        db.session.add(comment)
        db.session.commit()

        flash("Solution added successfully!", "success")
        return redirect(url_for('bug_detail', bug_id=bug.id))

    return render_template('bug_detail.html', bug=bug)

# ---------- RUN ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=False) # ✅ debug=False for production
