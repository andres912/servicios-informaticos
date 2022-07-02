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
from project.helpers.link_creator import LinkCreator
from project.models.association_tables.configuration_item_incident import (
    HardwareConfigurationItemIncident,
)
from project.models.comment import IncidentComment
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.incident import Incident, NullIncident
from project.models.status import STATUS_SOLVED
from project import db


class IncidentController(SolvableController):
    object_class = Incident
    null_object_class = NullIncident
    comment_class = IncidentComment


    @classmethod
    def create(cls, **kwargs):
        incident = super().create(**kwargs)
        for item in incident.get_items():
            comment = item.comment_class(
                text=f"Se ha creado el incidente con id {incident.id}, asociado a este ítem",
                object_id=item.id,
            )
            LinkCreator.create_incident_details_link(comment, incident.id)
            db.session.add(comment)

        db.session.commit()
        return incident