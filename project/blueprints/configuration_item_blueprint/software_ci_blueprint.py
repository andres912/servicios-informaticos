from flask import Blueprint, jsonify, request
from project.controllers.configuration_item_controller.software_ci_controller import (
    SoftwareConfigurationItemController,
)
from project.helpers.request_helpers import RequestValidator
from project.models.exceptions import (
    ExtraFieldsException,
    MissingFieldsException,
    ObjectNotFoundException,
)
from project.schemas.schemas import SoftwareConfigurationItemSchema

SOFTWARE_CI_ITEMS_ENDPOINT = "/configuration-items/software"

software_ci_blueprint = Blueprint("software_ci_blueprint", __name__)

item_schema = SoftwareConfigurationItemSchema()
items_schema = SoftwareConfigurationItemSchema(many=True)

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
    Creates a new Hardware Configuration Item
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
