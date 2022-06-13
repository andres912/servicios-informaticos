from project.controllers.base_controller import BaseController
from project.controllers.configuration_item_controller.hardware_ci_controller import (
    HardwareConfigurationItemController,
)
from project.controllers.configuration_item_controller.sla_ci_controller import (
    SLAConfigurationItemController,
)
from project.controllers.configuration_item_controller.software_ci_controller import (
    SoftwareConfigurationItemController,
)
from project.controllers.solvable_controller import SolvableController
from project.controllers.user_controller import UserController
from project.models.association_tables.configuration_item_incident import (
    HardwareConfigurationItemIncident,
)
from project.models.comment import IncidentComment
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.incident import Incident, NullIncident
from project.models.status import STATUS_SOLVED


class IncidentController(SolvableController):
    object_class = Incident
    null_object_class = NullIncident
    comment_class = IncidentComment
