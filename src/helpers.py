import jwt
import datetime
from . import env

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