from flask import Response
import json

def response(code, payload):
    return Response(json.dumps(payload), status=code, mimetype="application/json")

def payload(status, message, token=None):
    return {"status": status, "message": message, "auth_token": token}

def missing_parameter(parameter):
    return response(400, payload("fail", f"Missing required parameter: {parameter}"))

def conflict(field, data):
    return response(409, payload("fail", f"{field.capitalize()} '{data}' already exists"))

def not_found(field, data):
    return response(404, payload("fail", f"{field.capitalize()} '{data}' not found"))

def success(token=None):
    return response(200, payload("success", "👌", token))