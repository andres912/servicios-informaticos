from project.controllers.configuration_item_controller.configuration_item_controller import (
    ConfigurationItemController,
)
from project.models.configuration_item.sla_configuration_item import (
    SLAConfigurationItem,
)
from project import db
from project.models.versions.sla_item_version import SLAItemVersion


class SLAConfigurationItemController(ConfigurationItemController):
    object_class = SLAConfigurationItem
    null_object_class = None
    object_version_class = SLAItemVersion

