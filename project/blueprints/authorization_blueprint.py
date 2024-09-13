import jwt
import datetime
from typing import Dict, List, Tuple
from flask import Blueprint, request, jsonify, current_app
from functools import wraps

from project.schemas.schemas import UserSchema
from project.controllers.base_controller import ValidationError
from project.controllers.user_controller import UserController, InexistentBaseModelInstance
from project.models.user import User

user_schema = UserSchema()
authorization_blueprint = Blueprint("authorization_blueprint", __name__)

def user_required(roles_allowed: List = None):
    """
    Use this decorator around endpoints that need user authentication.
    "Bearer <token>" Authentication header is needed, where token is the
    JWT returned by the /login endpoint.
    See JWT https://jwt.io/

    The token has encoded the userid of the user which is logging in.

    E.g.
    curl --request GET 'localhost:5000/profile' \
         --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9 \
         .eyJpZCI6MSwiZXhwIjoxNjEzOTY4MzYzfQ.w2En8xdiRNTRQb6lFHci0j6z1fsVVPYCUYiux8qoOnY'
    """

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            auth = request.headers.get("Authorization")
            if auth and "Bearer" in auth:
                token = auth.split()[1]  # Bearer <token>
            if not token:
                return jsonify({"message": "Token is missing!"}), 401

            try:
                try:
                    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                except jwt.ExpiredSignatureError:  # TODO: test
                    return jsonify({"message": "Expired token"}), 500

                current_user = User.query.get(int(data["id"]))

                # user has at least one permission
                if roles_allowed and not any(
                    [role_allowed in current_user.permissions for role_allowed in roles_allowed]
                ):  # Checks if the current user has permissions to access the endpoint (roles_allowed is determined in each endpoint)
                    return (
                        jsonify({"message": "Not found"}),
                        404,
                    )  # we return 404 to not give away that the resource exists but it's hidden
            except BaseException:
                return jsonify({"message": "Token is invalid!"}), 401
            return f(current_user, *args, **kwargs)

        return decorated

    return token_required

@authorization_blueprint.route("/logged_in", methods=["GET"])
@user_required([])
def is_logged_in(current_app):
    """
    Endpoint to check if user is still logged in.
    Used to render pages in front-end.
    If user is not logged in, "token is invalid" answer is returned from user_required (from except BaseException).
    """
    return jsonify({"message": "Still logged in"})


@authorization_blueprint.route("/login", methods=["POST"])
def login():
    """
    Basic authorization works by sending an Authorization header
    with  "Basic username:password" where <username:password>
    is encoded in base64. Example for alevis:123456 is YWxldmlzOjEyMzQ1Ng==

    Login returns a JWT (https://jwt.io/) which the client can
    later use to identify itself using Bearer authentication
    (see function user_required)

    The token has encoded the userid of the user which is logging in.

    curl --request POST 'localhost:5000/login' \
         --header 'Authorization: Basic YWxldmlzOjEyMzQ1Ng=='
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return (
            jsonify({"error": "Invalid username or password"}),
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )
    try:
        user = UserController.load(email=auth.username, password=auth.password)
        token = jwt.encode(
            {"id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
            current_app.config["SECRET_KEY"],
        )
        UserController.set_as_logged(user)
    except InexistentBaseModelInstance as err:  # Inexistent username
        return jsonify(err.messages), 401, {"WWW-Authenticate": 'Basic realm="Login required!"'}
    except ValidationError as err:  # Incorrect password
        return jsonify(err.messages), 401, {"WWW-Authenticate": 'Basic realm="Login required!"'}
  
    return jsonify(
        {
            "token": token.decode(),
            "permissions": user.permissions,
            "user": {
            "id": user.id,
            "username": user.username,
            "role": {"id": user.role_id, "name": user.role.name},
            "email": user.email,
            "is_enabled": user.is_enabled,
            "is_deleted": user.is_deleted,
            }
        }
    )
