from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# In-memory user store (replace with a real DB later)
users = {
    'admin': {'id': 1, 'username': 'admin', 'password': 'admin123'},
}

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.id)

# Helper functions for Flask-Login user loader
def get_user_by_username(username):
    user_data = users.get(username)
    if user_data:
        return User(**user_data)
    return None

def get_user_by_id(user_id):
    for user_data in users.values():
        if str(user_data['id']) == str(user_id):
            return User(**user_data)
    return None


class HCSubscription(db.Model):
    __tablename__ = 'hc_subscription'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False)


class SubmitProblemsTable(db.Model):
    __tablename__ = 'submit_problems_table'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    concept = db.Column(db.String(100))
    correct = db.Column(db.Boolean)
    HCScore = db.Column(db.Integer)


class TestsMaster(db.Model):
    __tablename__ = 'tests_master'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100))
    sub_concept = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    status = db.Column(db.String(50))
    create_date = db.Column(db.DateTime)
