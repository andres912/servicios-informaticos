from project.controllers.base_controller import BaseController
from project.models.incident import Incident, NullIncident


class IncidentController(BaseController):
    object_class = Incident
    null_object_class = NullIncident

    @staticmethod
    def _verify_relations(new_commune: Incident) -> None:
        """
        Must be implemented.
        """
        pass
