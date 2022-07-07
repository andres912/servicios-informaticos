from flask import Blueprint, jsonify, request
from project.controllers.user_controller import UserController
from project.models.exceptions import ValidationError
from project.schemas.schemas import UserSchema
from project.blueprints.authorization_blueprint import user_required

# PASS (superadmin): serv-inf-0912

USERS_ENDPOINT = "/users"

user_schema = UserSchema()
users_schema = UserSchema(many=True)
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
        new_user = UserController.create(**request.json)
    except Exception as err:
        return jsonify(err.message), 422
    return user_schema.dump(new_user), 201


@users_blueprint.route(USERS_ENDPOINT, methods=["GET"])
def get_users():
    user = UserController.load_all()
    print(user_schema.dump(user))
    return jsonify(users_schema.dump(user))


@users_blueprint.route(f"{USERS_ENDPOINT}/<user_id>/profile", methods=["GET"])
def profile(user_id):
    user = UserController.load_by_id(user_id)
    print(user_schema.dump(user))
    return jsonify(user_schema.dump(user))
