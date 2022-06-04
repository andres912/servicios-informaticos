from project.controllers.configuration_item_controller.configuration_item_controller import ConfigurationItemController
from project.models.configuration_item.hardware_configuration_item import HardwareConfigurationItem
from project import db
from project.models.exceptions import ObjectNotFoundException


class HardwareConfigurationItemController(ConfigurationItemController):
    object_class = HardwareConfigurationItem
    null_object_class = None
    
    
        