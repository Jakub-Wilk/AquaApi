from flask import Blueprint, request
from ..responses import missing_parameter, success, unauthorized, not_found
from ..helpers import check_auth, get_mock_water_data
from ..database import mongo

get_bp = Blueprint("get", __name__)

@get_bp.route("/household", methods=["GET"])
def get_household():
    params = request.args
    # auth_user = check_auth(request.headers)
    # if not auth_user:
    #     return unauthorized("Valid token not found")
    if "username" in params.keys():
        username = params.get("username")
        household_data = mongo.db.households.find_one({"users": [username]})
        if not household_data:
            return not_found("household with user", username)
        # if auth_user not in household_data["users"]:
        #     return unauthorized("Users not in the same household")
        return success(household_data)
    elif "name" in params.keys():
        name = params.get("name")
        household_data = mongo.db.households.find_one({"name": name})
        if not household_data:
            return not_found("household", name)
        # if auth_user not in household_data["users"]:
        #     return unauthorized("User not in the household") 
        return success(household_data)
    else:
        return missing_parameter("household identifier")

@get_bp.route("/household/users", methods=["GET"])
def get_all_household_users():
    params = request.args
    # auth_user = check_auth(request.headers)
    # if not auth_user:
    #     return unauthorized("Valid token not found")
    if "name" in params.keys():
        name = params.get("name")
        household_data = mongo.db.households.find_one({"name": name})
        users = household_data["users"]
        # if auth_user not in users:
        #     return unauthorized("User not in the household")
        data = []
        for user in users:
            user_data = mongo.db.users.find_one({"username": user})
            user_data["_id"] = str(user_data["_id"])
            data.append(user_data)
        return success(data)
    else:
        return missing_parameter("household name")

@get_bp.route("/household/devices", methods=["GET"])
def get_all_household_devices():
    params = request.args
    # auth_user = check_auth(request.headers)
    # if not auth_user:
    #     return unauthorized("Valid token not found")
    if "name" in params.keys():
        name = params.get("name")
        household_data = mongo.db.households.find_one({"name": name})
        users = household_data["users"]
        devices = household_data["devices"]
        # if auth_user not in users:
        #     return unauthorized("User not in the household")
        data = []
        for device in devices:
            device_data = mongo.db.devices.find_one({"mac": device})
            device_data["_id"] = str(device_data["_id"])
            device_data["water_data"] = get_mock_water_data()
            data.append(device_data)
        return success(data)
    else:
        return missing_parameter("household name")

@get_bp.route("/user", methods=["GET"])
def get_user():
    params = request.args
    # auth_user = check_auth(request.headers)
    # if not auth_user:
    #     return unauthorized("Valid token not found")
    if "username" in params.keys():
        username = params.get("username")
        # auth_user_data = mongo.db.users.find_one({"username": auth_user})
        # if auth_user == username:
        #     return success(auth_user_data)
        user_data = mongo.db.users.find_one({"username": username})
        if not user_data:
            return not_found("user", username)
        # if auth_user_data["household"] != user_data["household"]:
        #     return unauthorized("Users not in the same household")
        user_data.pop("password")
        return success(user_data)
    else:
        # requesting_user_data = mongo.db.users.find_one({"username": auth_user})
        # return success(requesting_user_data)
        return missing_parameter("username")

@get_bp.route("/device", methods=["GET"])
def get_device():
    params = request.args
    # auth_user = check_auth(request.headers)
    # if not auth_user:
    #     return unauthorized("Valid token not found")
    if "mac" in params.keys():
        mac_address = params.get("mac")
        # auth_user_data = mongo.db.users.find_one({"username": auth_user})
        device_data = mongo.db.devices.find_one({"mac": mac_address})
        if not device_data:
            return not_found("device with mac", mac_address)
        # if auth_user_data["household"] != device_data["household"]:
        #     return unauthorized("User and device not in the same household")
        device_data["water_data"] = get_mock_water_data()
        return success(device_data)
    else:
        return missing_parameter("mac")

@get_bp.route("/coupons", methods=["GET"])
def get_coupons():
    # Coupons are stored in the database in the real app
    coupons = [
        {"shop": "Empik", "logo": "https://short.jakubwilk.xyz/aquathon_logo_E", "discount": "30%", "price": 5000, "description": "Lorem ipsum dolor sit amet"},
        {"shop": "Bonito", "logo": "https://short.jakubwilk.xyz/aquathon_logo_B", "discount": "10zł", "price": 500, "description": "consectetur adipiscing elit"},
        {"shop": "Levi's", "logo": "https://short.jakubwilk.xyz/aquathon_logo_L", "discount": "5%", "price": 1000, "description": "Phasellus dapibus sed nibh sed sollicitudin"},
        {"shop": "Stragan Zdrowia", "logo": "https://short.jakubwilk.xyz/aquathon_logo_SZ", "discount": "25zł", "price": 2000, "description": "Ut volutpat velit eget consequat iaculis"},
        {"shop": "ZIKO", "logo": "https://short.jakubwilk.xyz/aquathon_logo_Z", "discount": "7,5%", "price": 1500, "description": "Duis ac dolor eget sem vehicula semper"}
    ]
    return success(coupons)
    
@get_bp.route("/merch")
def get_merch():
    # Merch is stored in the database in the real app
    merch = [
        {"name": "Eko torba", "logo": "https://short.jakubwilk.xyz/aquathon_merch_T", "price": 4000},
        {"name": "Eko skarpetki", "logo": "https://short.jakubwilk.xyz/aquathon_merch_S", "price": 2500},
        {"name": "Eko koszulka", "logo": "https://short.jakubwilk.xyz/aquathon_merch_K", "price": 5000}
    ]
    return success(merch)