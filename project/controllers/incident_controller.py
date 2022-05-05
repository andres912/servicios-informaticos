from project.controllers.base_controller import BaseController
from project.controllers.user_controller import UserController
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
        incident.assign_user(taken_by=taken_by) # you don't need to save the incident again. Why? There is no why.
        
    
        

