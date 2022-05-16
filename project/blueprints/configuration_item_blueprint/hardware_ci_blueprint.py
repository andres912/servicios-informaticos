from flask import Blueprint, jsonify, request
from project.controllers.configuration_item_controller.hardware_ci_controller import (
    HardwareConfigurationItemController,
)
from project.helpers.request_validator import RequestValidator
from project.models.exceptions import (
    ExtraFieldsException,
    MissingFieldsException,
    ObjectNotFoundException,
)
from project.schemas.schemas import HardwareConfigurationItemSchema

HARDWARE_CI_ITEMS_ENDPOINT = "/configuration-items/hardware"

hardware_ci_blueprint = Blueprint("hardware_ci_blueprint", __name__)

item_schema = HardwareConfigurationItemSchema()
items_schema = HardwareConfigurationItemSchema(many=True)

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
        RequestValidator.verify_fields(request.json, POST_FIELDS)
    except (MissingFieldsException, ExtraFieldsException) as e:
        return jsonify({"errors": {e.cause: ",".join(e.invalid_fields)}}), 400

    item = HardwareConfigurationItemController.create(**request.json)
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
