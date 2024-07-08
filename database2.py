from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Person(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))

    def __init__(self, username, password, course_id):
        self.username = username
        self.password = password
        self.course_id = course_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'course_id': self.course_id
            # Add more fields as needed
        }

class Courses(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    course_fees = db.Column(db.Integer)

    def __init__(self, course_name, course_fees):
        self.course_name = course_name
        self.course_fees = course_fees


with app.app_context():
    db.create_all()

session = db.session

