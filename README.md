📌 Bug Tracking System

A secure, DevSecOps-enabled web application built with Flask to track, manage, and resolve software bugs efficiently.

🚀 Features

👤 User Registration & Login (Authentication)

🔐 Role-Based Access (Admin & User)

🐞 Bug Reporting with File Attachments

💬 Add Solutions to Bugs

📊 Admin Dashboard

🔔 Notification System

🌙 Dark Mode Support

📎 File Upload & Download

📧 Email Support (Password Reset)

🎨 Responsive UI (Bootstrap 5)

🛠 Tech Stack

Backend

Python 3

Flask

Flask-SQLAlchemy

Flask-Login

Flask-Mail

Frontend

HTML5

CSS3

JavaScript

Bootstrap 5

Font Awesome

Database

SQLite (Default)

Compatible with PostgreSQL/MySQL

📂 Project Structure
bug_tracking_system/
│
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── bugs.py
│   │   └── admin.py
│   │
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   └── uploads/
│   │
│   ├── models.py
│   └── __init__.py
│
├── config.py
├── main.py
└── README.md

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/bug-tracking-system.git
cd bug-tracking-system

2️⃣ Create Virtual Environment
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python main.py


Visit:

http://127.0.0.1:5000

🔐 Admin Access

To create an admin user:

Register normally

Manually update is_admin = True in the database

Or modify registration logic for first user.

🌙 Dark Mode

Toggle dark mode from the navbar.
All tables, forms, and cards support dark styling.

📎 File Uploads

Bug attachments supported

Solution attachments supported

Files stored in /static/uploads

🧠 Database Models

User

Bug

Solution

Notification

Uses SQLAlchemy ORM.

📬 Email Configuration

Update config.py:

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'

🔒 Security Features

Password Hashing

Login Protection

Role-Based Access Control

Secure File Handling

CSRF Ready (if using Flask-WTF)

📸 Screenshots

(Add screenshots here if needed)

🎯 Future Improvements

Charts Dashboard (Chart.js)

REST API

Docker Support

CI/CD Pipeline

JWT Authentication

Real-time Notifications

👨‍💻 Author

Developed as a DevSecOps-based academic project.

📄 License

This project is for educational purposes.