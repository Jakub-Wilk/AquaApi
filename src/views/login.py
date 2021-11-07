from flask import Blueprint, request
import bcrypt
from ..parsers import ParamParser
from ..responses import not_found, unauthorized, success
from ..helpers import generate_auth_token, generate_refresh_token
from ..database import mongo

login_bp = Blueprint("login", __name__)

@login_bp.route("", methods=["POST"])
def login():
    required_params = ["username", "password"]

    params = ParamParser(required_params, request.get_json())
    if not params.correct:
        return params.response
    
    username = params.get("username")
    password = params.get("password")

    user_data = mongo.db.users.find_one({"username": username})

    if not user_data:
        return not_found("user", username)
    
    if not bcrypt.checkpw(password.encode("utf-8"), user_data["password"]):
        return unauthorized("Password incorrect")
    
    # auth_token = generate_auth_token(username)
    # refresh_token = generate_refresh_token(username)

    return success() # None, auth_token, refresh_token)