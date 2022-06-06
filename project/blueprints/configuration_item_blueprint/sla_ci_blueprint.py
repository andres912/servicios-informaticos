from flask import Blueprint, jsonify, request
from project.controllers.configuration_item_controller.sla_ci_controller import (
    SLAConfigurationItemController,
)
from project.helpers.request_helpers import RequestValidator
from project.models.exceptions import (
    ExtraFieldsException,
    MissingFieldsException,
    ObjectNotFoundException,
)
from project.schemas.schemas import SLAConfigurationItemSchema

SLA_CI_ITEMS_ENDPOINT = "/configuration-items/sla"

sla_ci_blueprint = Blueprint("sla_ci_blueprint", __name__)

item_schema = SLAConfigurationItemSchema()
items_schema = SLAConfigurationItemSchema(many=True)

POST_FIELDS = {
    "name",
    "description",
    "service_type",
    "service_manager",
    "client",
    "starting_date",
    "ending_date",
    "measurement_unit",
    "measurement_value",
}

OPTIONAL_FIELDS = {"is_crucial"}


@sla_ci_blueprint.route(f"{SLA_CI_ITEMS_ENDPOINT}", methods=["GET"])
def get_configuration_items():
    """
    GET endpoint to get all SLA Configuration Items
    """
    conf_items = SLAConfigurationItemController.load_all()
    return jsonify(items_schema.dump(conf_items))


@sla_ci_blueprint.route(f"{SLA_CI_ITEMS_ENDPOINT}", methods=["POST"])
def create_item():
    """
    Creates a new SLA Configuration Item
    """
    try:
        RequestValidator.verify_fields(request.json, POST_FIELDS, OPTIONAL_FIELDS)
    except (MissingFieldsException, ExtraFieldsException) as e:
        return jsonify({"errors": {e.cause: ",".join(e.invalid_fields)}}), 400

    item = SLAConfigurationItemController.create(**request.json)
    return jsonify(item_schema.dump(item))


@sla_ci_blueprint.route(f"{SLA_CI_ITEMS_ENDPOINT}/<item_id>", methods=["PUT"])
def update_item(item_id):
    """
    PUT endpoint to update a SLA Configuration Item
    """
    try:
        RequestValidator.verify_fields(request.json, POST_FIELDS, OPTIONAL_FIELDS)
    except (MissingFieldsException, ExtraFieldsException) as e:
        return jsonify({"errors": {e.cause: ",".join(e.invalid_fields)}}), 400
    try:
        item = SLAConfigurationItemController.update(item_id=item_id, **request.json)
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"SLA Configuration Item with id {item_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(item_schema.dump(item))


@sla_ci_blueprint.route(f"{SLA_CI_ITEMS_ENDPOINT}/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """
    PUT endpoint to update a SLA Configuration Item
    """
    try:
        item = SLAConfigurationItemController.delete(id=item_id)
    except ObjectNotFoundException as e:
        return (
            jsonify(
                {
                    "errors": {
                        "object_not_found": f"SLA Configuration Item with id {item_id}"
                    }
                }
            ),
            404,
        )
    return jsonify(item_schema.dump(item))
