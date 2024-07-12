from flask import Blueprint, render_template, request
from source.publish_file import client
import json

courses = Blueprint("courses", __name__, url_prefix="/courses")

@courses.route("/", methods = ["GET", "POST", "PUT", "DELETE"])
def get_courses():
    if request.method == "POST":
        info = request.json
        client.publish("post1", json.dumps(info))

    if request.method == "PUT":
        info = request.json
        client.publish("put1", json.dumps(info))

    if request.method == "DELETE":
        info = request.json
        client.publish("delete1", json.dumps(info))
    return "This is courses page"



