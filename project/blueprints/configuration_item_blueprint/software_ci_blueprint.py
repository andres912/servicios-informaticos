from flask import Blueprint, jsonify, request
from project.controllers.configuration_item_controller.software_ci_controller import (
    SoftwareConfigurationItemController,
)
from project.helpers.request_helpers import ErrorHandler, RequestHelper, RequestValidator
from project.models.exceptions import (
    ExtraFieldsException,
    MissingFieldsException,
    ObjectNotFoundException,
)
from project.schemas.schemas import SoftwareConfigurationItemSchema

SOFTWARE_CI_ITEMS_ENDPOINT = "/configuration-items/software"

software_ci_blueprint = Blueprint("software_ci_blueprint", __name__)

item_schema = SoftwareConfigurationItemSchema()
items_schema = SoftwareConfigurationItemSchema(many=True, exclude=["versions"])
draft_schema = SoftwareConfigurationItemSchema(exclude=["current_version"])

POST_FIELDS = {"name", "description", "type", "provider", "software_version"}


@software_ci_blueprint.route(f"{SOFTWARE_CI_ITEMS_ENDPOINT}", methods=["GET"])
def get_configuration_items():
    """
    GET endpoint to get all Software Configuration Items
    """
    conf_items = SoftwareConfigurationItemController.load_all()
    return jsonify(items_schema.dump(conf_items))


@software_ci_blueprint.route(f"{SOFTWARE_CI_ITEMS_ENDPOINT}", methods=["POST"])
def create_item():
    """
    Creates a new Software Configuration Item
    """
    try:
        RequestValidator.verify_fields(request.json, POST_FIELDS)
    except (MissingFieldsException, ExtraFieldsException) as e:
        return jsonify({"errors": {e.cause: ",".join(e.invalid_fields)}}), 400

    item = SoftwareConfigurationItemController.create(**request.json)
    return jsonify(item_schema.dump(item))


@software_ci_blueprint.route(f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>", methods=["GET"])
def get_item(item_id):
    """
    Creates a new Software Configuration Item
    """
    item = SoftwareConfigurationItemController.load_by_id(item_id)
    return jsonify(item_schema.dump(item))


@software_ci_blueprint.route(f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>", methods=["PUT"])
def update_item(item_id):
    """
    PUT endpoint to update a Software Configuration Item
    """
    try:
        RequestValidator.verify_fields(request.json, POST_FIELDS)
    except (MissingFieldsException, ExtraFieldsException) as e:
        return jsonify({"errors": {e.cause: ",".join(e.invalid_fields)}}), 400
    try:
        item = SoftwareConfigurationItemController.update(
            item_id=item_id, **request.json
        )
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"Software Configuration Item with id {item_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(item_schema.dump(item))


@software_ci_blueprint.route(
    f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>", methods=["DELETE"]
)
def delete_item(item_id):
    """
    PUT endpoint to update a Software Configuration Item
    """
    try:
        item = SoftwareConfigurationItemController.delete(id=item_id)
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"Software Configuration Item with id {item_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(item_schema.dump(item))

@software_ci_blueprint.route(f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>/restore", methods=["POST"])
def restore_item_version(item_id):
    """
    Creates a new Software Configuration Item
    """
    try:
        version = request.json.get("version")
        item = SoftwareConfigurationItemController.restore_item_version(item_id, version)
        return jsonify(item_schema.dump(item))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)

@software_ci_blueprint.route(f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>/version", methods=["POST"])
def create_item_version(item_id):
    """
    Creates a new Software Configuration Item
    """
    try:
        correct_request = RequestHelper.correct_dates(request.json)
        new_item = SoftwareConfigurationItemController.create_new_item_version(item_id, **correct_request)
        return jsonify(item_schema.dump(new_item))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)

def update_item_draft(item, change_id, request_json):
    draft = item.draft
    if change_id != draft.change_id:
        return (
            jsonify(
                {"errors": {"change_id": "Draft does not match requested change_id"}}
            ),
            400,
        )

    correct_request = RequestHelper.correct_dates(request_json)
    SoftwareConfigurationItemController.update_item_draft(item.id, **correct_request)


def create_new_draft(item, change_id, request_json):
    correct_request = RequestHelper.correct_dates(request_json)
    draft = SoftwareConfigurationItemController.create_draft(item.id, change_id, **correct_request)
    return draft


@software_ci_blueprint.route(
    f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>/draft", methods=["POST"]
)
def create_item_draft(item_id):
    try:
        change_id = int(request.args["change_id"])
        item = SoftwareConfigurationItemController.load_by_id(item_id)

        if item.has_draft():
            update_item_draft(item, change_id, request.json)
            return jsonify(draft_schema.dump(item))
        else:
            create_new_draft(item, change_id, request.json)
            return jsonify(draft_schema.dump(item))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)


@software_ci_blueprint.route(
    f"{SOFTWARE_CI_ITEMS_ENDPOINT}/<item_id>/draft", methods=["GET"]
)
def get_item_draft(item_id):
    try:
        item = SoftwareConfigurationItemController.load_by_id(item_id)
        if item.has_draft():
            change_id = int(request.args["change_id"])
            if change_id != item.draft.change_id:
                return (
                    jsonify(
                        {
                            "errors": {
                                "change_id": "Draft does not match requested change_id"
                            }
                        }
                    ),
                    400,
                )
            return jsonify(draft_schema.dump(item))
        return jsonify(item_schema.dump(item))

    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)