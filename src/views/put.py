import re
from flask import Blueprint, request
from ..responses import missing_parameter, success, not_found
from ..parsers import ParamParser
from ..helpers import check_auth
from ..database import mongo

put_bp = Blueprint("put", __name__)

@put_bp.route("/task", methods=["PUT"])
def finish_task():
    possible_tasks = ["meat", "shower", "teeth", "dishes"]

    required_params = ["username", "type"]

    params = ParamParser(required_params, request.get_json())
    if not params.correct:
        return params.response

    task_type = params.get("type")
    username = params.get("username")
    
    if task_type not in possible_tasks:
        return not_found("task type", task_type)

    user_data = mongo.db.users.find_one({"username": username})
    if not user_data:
        return not_found("user", username)
    value = 0
    for task in user_data["active_tasks"]:
        if task["type"] == task_type:
            value = task["reward"]
            break
    
    if value == 0:
        return not_found("task", task_type)
    
    mongo.db.users.update_one({"username": username, "active_tasks": {"$elemMatch": {"type": task_type}}}, {"$inc": {"droplets": value}, "$set": {"active_tasks.$.completed": True}})

    return success()
    



