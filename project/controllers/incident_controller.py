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
from project.models.exceptions import BadQueryException, ObjectNotFoundException
from project.models.incident import Incident, NullIncident


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
            raise BadQueryException("Username is required.")
        return Incident.query.filter_by(created_by=username).all()

    @staticmethod
    def load_incidents_assigned_to_user(username: str = "") -> None:
        if not username:
            raise BadQueryException("Username is required.")
        return Incident.query.filter_by(taken_by=username).all()

    @staticmethod
    def load_assigned_incidents() -> None:
        return Incident.query.filter(Incident.taken_by != None).all()

    @staticmethod
    def load_unassigned_incidents() -> None:
        return Incident.query.filter(Incident.taken_by == None).all()

    @classmethod
    def assign_incident_to_user(cls, incident_id: int, taken_by: str) -> None:
        user = UserController.load_by_username(username=taken_by)
        if not user:
            raise ObjectNotFoundException("User not found")
        incident = cls.load_by_id(incident_id)
        if not incident:
            raise ObjectNotFoundException("Incident not found")
        incident.assign_user(
            taken_by=taken_by
        )  # you don't need to save the incident again. Why? There is no why.

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
        modified_parameters = cls.add_configuration_items(**kwargs)
        return super().create(**modified_parameters)

    @classmethod
    def add_configuration_items(cls, **kwargs):
        hardware_ci_ids = kwargs.get("hardware_configuration_items", [])
        software_ci_ids = kwargs.get("software_configuration_items", [])
        sla_ci_ids = kwargs.get("sla_configuration_items", [])
        hardware_configuration_items = [
            HardwareConfigurationItemController.load_by_id(item_id)
            for item_id in hardware_ci_ids
        ]
        software_configuration_items = [
            SoftwareConfigurationItemController.load_by_id(item_id)
            for item_id in software_ci_ids
        ]
        sla_configuration_items = [
            SLAConfigurationItemController.load_by_id(item_id) for item_id in sla_ci_ids
        ]

        kwargs["hardware_configuration_items"] = hardware_configuration_items
        kwargs["software_configuration_items"] = software_configuration_items
        kwargs["sla_configuration_items"] = sla_configuration_items
        return kwargs

