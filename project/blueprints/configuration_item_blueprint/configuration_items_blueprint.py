from flask import Blueprint, jsonify
from project.controllers.configuration_item_controller.hardware_ci_controller import (
    HardwareConfigurationItemController,
)
from project.controllers.configuration_item_controller.software_ci_controller import (
    SoftwareConfigurationItemController,
)
from project.controllers.configuration_item_controller.sla_ci_controller import (
    SLAConfigurationItemController,
)
from project.schemas.schemas import ReducedConfigurationItemSchema


CONFIGURATION_ITEMS_ENDPOINT = "/configuration-items"

ci_blueprint = Blueprint("ci_blueprint", __name__)

# item_schema = ConfigurationItemSchema(only=["name", "id", "item_class"])
items_schema = ReducedConfigurationItemSchema(many=True)


@ci_blueprint.route(f"{CONFIGURATION_ITEMS_ENDPOINT}/names", methods=["GET"])
def get_configuration_items_names():
    """
    GET endpoint to get all Hardware Configuration Items
    """
    hardware_conf_items = HardwareConfigurationItemController.load_all()
    software_conf_items = SoftwareConfigurationItemController.load_all()
    sla_conf_items = SLAConfigurationItemController.load_all()
    conf_items = hardware_conf_items + software_conf_items + sla_conf_items
    dump = items_schema.dump(conf_items)
    name_list = {
        "items": [{"value": item["name"], "label": item["name"]} for item in dump]
    }
    return jsonify(name_list)


@ci_blueprint.route(f"{CONFIGURATION_ITEMS_ENDPOINT}/all", methods=["GET"])
def get_configuration_items():
    """
    GET endpoint to get all Hardware Configuration Items
    """
    hardware_conf_items = HardwareConfigurationItemController.load_all()
    software_conf_items = SoftwareConfigurationItemController.load_all()
    sla_conf_items = SLAConfigurationItemController.load_all()
    conf_items = hardware_conf_items + software_conf_items + sla_conf_items
    items_info = [
        {
            "name": item.current_version.name + " (" + item.item_type + ")",
            "value": len(item.incidents),
        }
        for item in conf_items
    ]
    items_info.sort(key=lambda x: x["value"], reverse=True)
    items_info = items_info[:5]
    item_list = {"items": items_info}
    return jsonify(item_list)
