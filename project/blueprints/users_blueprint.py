from flask import Blueprint, jsonify, request
from project.controllers.user_controller import UserController
from project.models.exceptions import ValidationError
from project.schemas.schemas import UserSchema
from project.blueprints.authorization_blueprint import user_required

# PASS (superadmin): serv-inf-0912

USERS_ENDPOINT = "/users"

user_schema = UserSchema()
users_blueprint = Blueprint("users_blueprint", __name__)


@users_blueprint.route(f"{USERS_ENDPOINT}", methods=["POST"])
# @user_required([EDIT_USER])
def register():
    """
    Creates a new user. If no role is passed, "user" role will be applied
    Returns HTTP code 201 (created)
    """

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    role_id = request.json["role_id"] if "role_id" in request.json else None
    name = request.json["name"] if "name" in request.json else None
    lastname = request.json["lastname"] if "lastname" in request.json else None

    try:
        new_user = UserController.create(
            username=username,
            email=email,
            password=password,
            role_id=role_id,
            name=name,
            lastname=lastname,
        )
        UserController.save(new_user)
    except ValidationError as err:
        return jsonify(err.messages), 422
    return user_schema.dump(new_user)


@users_blueprint.route(USERS_ENDPOINT, methods=["GET"])
# @user_required([EDIT_USER])
def get_users():
    return "OK"


@users_blueprint.route("/profile", methods=["GET"])
@user_required([])
def profile(current_user):
    return jsonify(user_schema.dump(current_user))
