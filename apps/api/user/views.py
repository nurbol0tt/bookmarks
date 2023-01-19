from flask import Blueprint, jsonify

bl = Blueprint('user', __name__, url_prefix="/user")


@bl.post("/register")
def register():
    return jsonify({"message": "you register"})


@bl.get("/")
def me():
    return jsonify({"message": "Hello World"})
