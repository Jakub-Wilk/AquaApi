from flask import Flask, request
from flask_pymongo import PyMongo
import jwt
import datetime
from . import env
from .responses import success, conflict, not_found
from .parsers import ParamParser

app = Flask(__name__)
app.config["MONGO_URI"] = env.mongo_uri
app.config["SECRET_KEY"] = env.secret_key

mongo = PyMongo(app)

def generate_jwt_token(username):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        "iat": datetime.datetime.utcnow(),
        "sub": username
    }
    return jwt.encode(
        payload,
        app.config.get("SECRET_KEY"),
        algorithm="HS256"
    )

def validate_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, app.config.get("SECRET_KEY"))
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

@app.route("/register/household", methods=["POST"])
def register_household():
    required_params = ["name"]

    params = ParamParser(required_params, request.get_json())
    if not params.correct:
        return params.response

    name = params.get("name")

    household_data = mongo.db.households.find_one({"name": name})

    if household_data:
        return conflict("household", name)
    mongo.db.households.insert_one(
        {
            "name": name,
            "users": [],
            "devices": []
        }
    )
    return success()

