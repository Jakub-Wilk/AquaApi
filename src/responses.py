from flask import Response
import json

def payload(status, message, data=None, auth_token=None, refresh_token=None):
    return {"status": status, "message": message, "data": data, "auth_token": auth_token, "refresh_token": refresh_token}

def response(code, payload):
    return Response(json.dumps(payload), status=code, mimetype="application/json")

def missing_parameter(parameter):
    return response(400, payload("fail", f"Missing required parameter: {parameter}"))

def conflict(field, data):
    return response(409, payload("fail", f"{field.capitalize()} '{data}' already exists"))

def not_found(field, data):
    return response(404, payload("fail", f"{field.capitalize()} '{data}' not found"))

def unauthorized(message):
    return response(401, payload("fail", message))

def success(data=None, auth_token=None, refresh_token=None):
    if data and type(data) is dict and "_id" in data.keys():
        data["_id"] = str(data["_id"])
    return response(200, payload("success", "👌", data, auth_token, refresh_token))