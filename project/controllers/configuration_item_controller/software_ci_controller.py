from project.controllers.configuration_item_controller.configuration_item_controller import ConfigurationItemController
from project.models.configuration_item.software_configuration_item import SoftwareConfigurationItem
from project import db


class SoftwareConfigurationItemController(ConfigurationItemController):
    object_class = SoftwareConfigurationItem
    null_object_class = None

    