from flask import Flask, jsonify
from source.users import users
from source.database2 import db, Person
from source.courses import courses

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
app.register_blueprint(courses)
app.register_blueprint(users)

@app.route("/")
def home():
    return "My name is Kowshik"

@app.route("/course/<int:course_id>")
def get_course(course_id):
    courses = db.session.query(Person).filter(Person.course_id == course_id).all()
    course_json = [course.to_dict() for course in courses]
    return jsonify(course_json)
# app.run()
