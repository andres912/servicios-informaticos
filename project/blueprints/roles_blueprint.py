from flask import Blueprint, jsonify, request
from project.controllers.role_controller import RoleController
from project.controllers.base_controller import InexistentBaseModelInstance, ValidationError
from project.schemas.schemas import RoleSchema

ROLES_ENDPOINT = "/roles"

roles_blueprint = Blueprint("roles_blueprint", __name__)
role_schema = RoleSchema()

@roles_blueprint.route(ROLES_ENDPOINT, methods=["POST"])
#@user_required([EDIT_ROLE])
def post_role():
    """
    POST endpoint for Role.
    """
    name = request.json["name"]
    permissions = request.json["permissions"]
    try:
        new_role = RoleController.create(name=name, permissions=permissions)
        RoleController.save(new_role)
    except ValidationError as err:
        return jsonify(err.messages), 422
    return role_schema.dump(new_role)
