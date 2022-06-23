from flask import Blueprint, jsonify, request
from project.controllers.known_error_controller import KnownErrorController
from project.helpers.known_error_request_helper import KnownErrorRequestHelper
from project.schemas.schemas import KnownErrorSchema
from project.models.exceptions import (
    ObjectNotFoundException,
)


KNOWN_ERRORS_ENDPOINT = "/errors"

known_error_blueprint = Blueprint("known_error_blueprint", __name__)


error_schema = KnownErrorSchema()
errors_schema = KnownErrorSchema(many=True)

@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}", methods=["GET"])
def get_errors():
    """
    GET endpoint to get all Errors.
    """
    errors = KnownErrorController.load_all()
    return jsonify(errors_schema.dump(errors))


@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}/<error_id>", methods=["GET"])
def get_error(error_id):
    """
    GET endpoint to get all Errors.
    """
    try:
        error = KnownErrorController.load_by_id(error_id)
        return error_schema.dump(error), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}/<error_id>", methods=["PUT"])
def update_known_error(error_id):
    """
    PUT endpoint to update a Known Error
    """
    try:
        error = KnownErrorController.update(
            known_error_id = error_id, **request.json
        )
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"Known Error with id {error_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(error_schema.dump(error))


#* Ver esto despues, debe ser necesario para el tag de los known error del user logueado
'''
@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}/<user_id>", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_user_known_errors(user_id):
    """
    GET endpoint to get all Errors from a specific user.
    """
    errors = KnownErrorController.load_known_errors_assigned_to_user(username=user_id)
    return jsonify(errors_schema.dump(errors))
'''


#? ok ?
@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}", methods=["POST"])
# @user_required([EDIT_DISTRIBUTOR])
def create_known_error():
    """
    POST endpoint to create a new Error.
    """
    correct_request = KnownErrorRequestHelper.create_error_request(request.json)
    error = KnownErrorController.create(**correct_request)
    return error_schema.dump(error)

