import jwt
import datetime
from . import env
from .database import mongo

# Auth

def generate_jwt_token(username, lifetime):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=lifetime),
        "iat": datetime.datetime.utcnow(),
        "sub": username
    }
    return jwt.encode(
        payload,
        env.secret_key,
        algorithm="HS256"
    )

def generate_auth_token(username):
    return generate_jwt_token(username, 10)

def generate_refresh_token(username):
    return generate_jwt_token(username, 43200)

def validate_jwt_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, env.secret_key, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def check_auth_header(auth_header):
    if not auth_header:
        return False
    token = auth_header.split(" ")[1]
    token_payload = validate_jwt_token(token)
    if not token_payload:
        return False
    return token_payload

def check_auth(headers):
    auth_header = headers.get("Authorization")
    if not auth_header:
        return False
    token_user = check_auth_header(auth_header)
    if not token_user:
        return False
    return token_user

# Tasks

def generate_mock_tasks():
    # Tasks are generated based on user's history in the real app
    return [
        {
            "name": "Weź prysznic zamiast kąpieli",
            "type": "shower",
            "reward": 40
        },
        {
            "name": "Umyj zęby z zakręconym kranem",
            "type": "teeth",
            "reward": 10
        },
        {
            "name": "Umyj naczynia gdy zmywarka będzie pełna",
            "type": "dishes",
            "reward": 20
        },
        {
            "name": "Nie jedz mięsa",
            "type": "meat",
            "reward": 50
        }
    ]

def get_mock_water_data():
    # In the real app this data is fetched from water meters on individual devices
    return [
        {
            "time": 1636254060,
            "volume": 20
        },
        {
            "time": 1636255030,
            "volume": 40,
        },
        {
            "time": 1636256260,
            "volume": 16
        },
        {
            "time": 1636257860,
            "volume": 53
        },
        {
            "time": 1636259000,
            "volume": 24
        },
        {
            "time": 1636259560,
            "volume": 37
        },
        {
            "time": 1636261265,
            "volume": 28
        }
    ]