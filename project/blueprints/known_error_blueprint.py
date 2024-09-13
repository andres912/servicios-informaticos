from flask import Blueprint, jsonify, request
from project.controllers.known_error_controller import KnownErrorController
from project.helpers.known_error_request_helper import KnownErrorRequestHelper
from project.schemas.schemas import KnownErrorSchema
from project.models.exceptions import (
    ObjectNotFoundException,
)
from project.helpers.request_helpers import (
    RequestHelper,
    RequestValidator,
    ErrorHandler,
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


@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}/<error_id>/version", methods=["POST"])
def create_error_version(error_id):
    """
    Creates a new Version for the Known Error
    """
    try:
        correct_request = RequestHelper.correct_dates(request.json)
        new_error = KnownErrorController.create_new_known_error_version(
            error_id, **correct_request
        )
        return jsonify(error_schema.dump(new_error))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)


@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}/<error_id>/restore", methods=["POST"])
def restore_error_version(error_id):
    """
    Restores a Known Error Version
    """
    try:
        version = request.json.get("version")
        error = KnownErrorController.restore_known_error_version(
            error_id, version
        )
        return jsonify(error_schema.dump(error))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)



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


@known_error_blueprint.route(f"{KNOWN_ERRORS_ENDPOINT}/incident", methods=["POST"])
# @user_required([EDIT_DISTRIBUTOR])
def add_incident_to_error():
    """
    POST endpoint to create a new Error.
    """
    error_id = request.json.get("error_id")
    incident_name = request.json.get("incident_name")
    known_error = KnownErrorController.add_incident_to_error(error_id, incident_name)
    return jsonify(error_schema.dump(known_error))
