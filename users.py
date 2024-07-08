from flask import Blueprint, render_template, request
from publish_file import client
from logs import logger
import json

users = Blueprint("users", __name__, url_prefix="/users")

@users.route("/", methods = ["GET", "POST", "PUT", "DELETE"])
def get_users():
    if request.method == "GET":
        logger.info("GET request is fetched from users")
    if request.method == "POST":
        info = request.json
        logger.info("POST request is used from users")
        client.publish("post", json.dumps(info))

    if request.method == "PUT":
        info = request.json
        logger.info("PUT request is used from users")
        client.publish("put", json.dumps(info))

    if request.method == "DELETE":
        info = request.json
        logger.info("DELETE request is used from users")
        client.publish("delete", json.dumps(info))

    return "This is users page"




