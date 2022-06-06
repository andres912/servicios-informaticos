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
from project.controllers.user_controller import UserController
from project.models.association_tables.configuration_item_incident import (
    HardwareConfigurationItemIncident,
)
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.incident import Incident, NullIncident
from project.models.status import STATUS_SOLVED


class IncidentController(BaseController):
    object_class = Incident
    null_object_class = NullIncident

    @staticmethod
    def _verify_relations(incident: Incident) -> None:
        """
        Must be implemented.
        """
        pass

    @staticmethod
    def load_incidents_created_by_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return Incident.query.filter_by(created_by=username).all()

    @staticmethod
    def load_incidents_assigned_to_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return Incident.query.filter_by(taken_by=username).all()

    @classmethod
    def assign_to_user(cls, object_id: int, taken_by: str) -> None:
        user = UserController.load_by_username(username=taken_by)
        if not user:
            raise ObjectNotFoundException("User not found")
        incident = cls.load_by_id(object_id)
        if not incident:
            raise ObjectNotFoundException("Incident not found")
        incident.assign_user(
            taken_by=taken_by
        )

    @classmethod
    def relate_incident_to_hardware_configuration_item(
        cls, incident_id: int, hardware_configuration_item_id: int
    ) -> None:
        incident = cls.load_by_id(incident_id)
        if not incident:
            raise ObjectNotFoundException("Incident not found")
        hardware_configuration_item = HardwareConfigurationItemController.load_by_id(
            hardware_configuration_item_id
        )
        if not hardware_configuration_item:
            raise ObjectNotFoundException("Hardware Configuration Item not found")
        hardware_configuration_item.incidents.append(incident)

    @classmethod
    def create(cls, **kwargs) -> Incident:
        return super().create(**kwargs)


