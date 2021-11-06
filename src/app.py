from flask import Flask, request
from flask_pymongo import PyMongo
import jwt
import datetime
import bcrypt
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

@app.route("/register/user", methods=["POST"])
def register_user():
    required_params = ["username", "password", "household"]

    params = ParamParser(required_params, request.get_json()
)
    if not params.correct:
        return params.response

    username = params.get("username")
    password = params.get("password")
    household = params.get("household")

    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    household_data = mongo.db.households.find_one({"name": household})
    user_data = mongo.db.users.find_one({"username": username})
    if not household_data:
        return not_found("household", household)
    if user_data:
        return conflict("user", username)

    mongo.db.households.update_one(
        {"name": household},
        {"$push":
            {"users": username}
        }
    )
    mongo.db.users.insert_one(
        {
            "username": username,
            "password": password,
            "household": household,
            "droplets": 0,
            "active_tasks": []
        }
    )

    auth_token = generate_jwt_token(username)

    return success(auth_token)

@app.route("/register/device", methods=["POST"])
def register_device():
    possible_devices = ["washing_machine", "sink", "bathtub", "shower", "dishwasher", "toilet", "hose"]

    required_params = ["mac", "name", "household", "type"]

    params = ParamParser(required_params, request.get_json())
    if not params.correct:
        return params.response

    mac_address = params.get("mac")
    name = params.get("name")
    household = params.get("household")
    device_type = params.get("type")

    if device_type not in possible_devices:
        return not_found("device type", device_type)

    household_data = mongo.db.households.find_one({"name": household})
    device_data = mongo.db.users.find_one({"mac": mac_address})
    if not household_data:
        return not_found("household", household)
    if device_data:
        return conflict("mac adress", mac_address)

    mongo.db.households.update_one(
        {"name": household},
        {"$push": 
            {"devices": mac_address}
        }
    )

    mongo.db.devices.insert_one(
        {
            "mac": mac_address,
            "name": name,
            "household": household,
            "type": device_type,
            "water_data": []
        }
    )
    return success()

