from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Bug , Comment

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

# ---------- AUTH ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        # First user becomes admin
        is_admin = False
        if User.query.count() == 0:
            is_admin = True

        user = User(
            username=username,
            password=password,
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            session['is_admin'] = user.is_admin

            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ---------- BUG MODULE ----------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    bugs = Bug.query.all()
    return render_template('dashboard.html', bugs=bugs)

@app.route('/add-bug', methods=['GET', 'POST'])
def add_bug():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        bug = Bug(
            title=request.form['title'],
            description=request.form['description'],
            severity=request.form['severity'],
            reported_by=session['user']
        )
        db.session.add(bug)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_bug.html')

@app.route('/update-status/<int:bug_id>', methods=['POST'])
def update_status(bug_id):
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))

    bug = Bug.query.get(bug_id)
    bug.status = request.form['status']
    db.session.commit()
    return redirect(url_for('dashboard'))

# ---------- BUG DETAIL & COMMENTS ----------
@app.route('/bug/<int:bug_id>', methods=['GET', 'POST'])
def bug_detail(bug_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    bug = Bug.query.get(bug_id)
    comments = Comment.query.filter_by(bug_id=bug_id).all()

    if request.method == 'POST':
        comment = Comment(
            content=request.form['content'],
            author=session['user'],
            bug_id=bug_id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('bug_detail', bug_id=bug_id))

    return render_template('bug_detail.html', bug=bug, comments=comments)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)

