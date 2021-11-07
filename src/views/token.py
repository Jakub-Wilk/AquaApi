from flask import Blueprint, request
from ..responses import missing_parameter, unauthorized, success
from ..helpers import check_auth_header, generate_auth_token

token_bp = Blueprint("token", __name__)

@token_bp.route("/refresh", methods=["POST"])
def refresh_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return missing_parameter("authorization header")
    token_user = check_auth_header(auth_header)
    if not token_user:
        return unauthorized("Token invalid")
    new_auth_token = generate_auth_token(token_user)
    return success(None, new_auth_token)