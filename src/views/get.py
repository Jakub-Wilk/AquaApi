from flask import Blueprint, request
from ..responses import missing_parameter, success, unauthorized, not_found
from ..helpers import check_auth
from ..database import mongo

get_bp = Blueprint("get", __name__)


@get_bp.route("/household", methods=["GET"])
def get_household():
    params = request.args
    auth_user = check_auth(request.headers)
    if not auth_user:
        return unauthorized("Valid token not found")
    if "username" in params.keys():
        username = params.get("username")
        household_data = mongo.db.households.find_one({"users": [username]})
        if not household_data:
            return not_found("household with user", username)
        if auth_user not in household_data["users"]:
            return unauthorized("Users not in the same household")
        return success(household_data)
    elif "name" in params.keys():
        name = params.get("name")
        household_data = mongo.db.households.find_one({"name": name})
        if not household_data:
            return not_found("household", name)
        if auth_user not in household_data["users"]:
            return unauthorized("User not in the household")
        return success(household_data)
    else:
        return missing_parameter("household identifier")
