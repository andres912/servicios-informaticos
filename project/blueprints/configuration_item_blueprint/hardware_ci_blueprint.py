from flask import Blueprint, jsonify, request
from project.controllers.configuration_item_controller.hardware_ci_controller import (
    HardwareConfigurationItemController,
)
from project.helpers.request_helpers import (
    RequestHelper,
    RequestValidator,
    ErrorHandler,
)
from project.models.exceptions import (
    ExtraFieldsException,
    MissingFieldsException,
    ObjectNotFoundException,
)
from project.schemas.schemas import (
    HardwareConfigurationItemSchema,
    HardwareItemVersionSchema,
)

HARDWARE_CI_ITEMS_ENDPOINT = "/configuration-items/hardware"

hardware_ci_blueprint = Blueprint("hardware_ci_blueprint", __name__)

item_schema = HardwareConfigurationItemSchema()
items_schema = HardwareConfigurationItemSchema(many=True, exclude=["versions"])
draft_schema = HardwareItemVersionSchema()

POST_FIELDS = {
    "name",
    "description",
    "type",
    "price",
    "purchase_date",
    "serial_number",
    "manufacturer",
}


@hardware_ci_blueprint.route(f"{HARDWARE_CI_ITEMS_ENDPOINT}", methods=["GET"])
def get_configuration_items():
    """
    GET endpoint to get all Hardware Configuration Items
    """
    conf_items = HardwareConfigurationItemController.load_all()
    return jsonify(items_schema.dump(conf_items))


@hardware_ci_blueprint.route(f"{HARDWARE_CI_ITEMS_ENDPOINT}", methods=["POST"])
def create_item():
    """
    Creates a new Hardware Configuration Item
    """
    try:
        RequestValidator.verify_fields(
            request.json, POST_FIELDS, optional_fields={"item_family_id", "version"}
        )
        item = HardwareConfigurationItemController.create(**request.json)
        return jsonify(item_schema.dump(item))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)


@hardware_ci_blueprint.route(f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>", methods=["GET"])
def get_item(item_id):
    """
    Creates a new Hardware Configuration Item
    """
    item = HardwareConfigurationItemController.load_by_id(item_id)
    return jsonify(item_schema.dump(item))


@hardware_ci_blueprint.route(f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>", methods=["PUT"])
def update_item(item_id):
    """
    PUT endpoint to update a Hardware Configuration Item
    """
    try:
        RequestValidator.verify_fields(request.json, POST_FIELDS)
    except (MissingFieldsException, ExtraFieldsException) as e:
        return jsonify({"errors": {e.cause: ",".join(e.invalid_fields)}}), 400
    try:
        item = HardwareConfigurationItemController.update(
            item_id=item_id, **request.json
        )
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"Hardware Configuration Item with id {item_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(item_schema.dump(item))


@hardware_ci_blueprint.route(
    f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>", methods=["DELETE"]
)
def delete_item(item_id):
    """
    PUT endpoint to update a Hardware Configuration Item
    """
    try:
        item = HardwareConfigurationItemController.delete(id=item_id)
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"Hardware Configuration Item with id {item_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(item_schema.dump(item))


@hardware_ci_blueprint.route(
    f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>/restore", methods=["POST"]
)
def restore_item_version(item_id):
    """
    Creates a new Hardware Configuration Item
    """
    try:
        version = request.json.get("version")
        item = HardwareConfigurationItemController.restore_item_version(
            item_id, version
        )
        return jsonify(item_schema.dump(item))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)


@hardware_ci_blueprint.route(
    f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>/version", methods=["POST"]
)
def create_item_version(item_id):
    """
    Creates a new Hardware Configuration Item
    """
    try:
        correct_request = RequestHelper.correct_dates(request.json)
        new_item = HardwareConfigurationItemController.create_new_item_version(
            item_id, **correct_request
        )
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
    return draft.update(**correct_request)


def create_new_draft(item, change_id, request_json):
    correct_request = RequestHelper.correct_dates(request_json)
    draft = HardwareConfigurationItemController.create_draft(item.id, change_id, **correct_request)
    return draft


@hardware_ci_blueprint.route(
    f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>/draft", methods=["POST"]
)
def create_item_draft(item_id):
    import pdb; pdb.set_trace()
    try:
        change_id = int(request.args["change_id"])
        item = HardwareConfigurationItemController.load_by_id(item_id)

        if item.has_draft():
            draft = update_item_draft(item, change_id, request.json)
            return jsonify(draft_schema.dump(draft))
        else:
            draft = create_new_draft(item, change_id, request.json)
            return jsonify(draft_schema.dump(draft))
    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)


@hardware_ci_blueprint.route(
    f"{HARDWARE_CI_ITEMS_ENDPOINT}/<item_id>/draft", methods=["GET"]
)
def get_item_draft(item_id):
    try:
        item = HardwareConfigurationItemController.load_by_id(item_id)
        if item.has_draft():
            draft = item.draft
            change_id = int(request.args["change_id"])
            if change_id != draft.change_id:
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

            return jsonify(draft_schema.dump(draft))
        return jsonify(item_schema.dump(item))

    except Exception as e:
        return ErrorHandler.determine_http_error_response(e)