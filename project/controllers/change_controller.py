from project.controllers.base_controller import BaseController
from project.controllers.incident_controller import IncidentController
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.change import Change, NullChange

from project.controllers.problem_controller import ProblemController
from project.controllers.user_controller import UserController
from project.models.association_tables.incident_change import IncidentChange
from project.models.association_tables.problem_change import ProblemChange


class ChangeController(BaseController):
    object_class = Change
    null_object_class = NullChange

    @staticmethod
    def _verify_relations(change: Change) -> None:
        """
        Must be implemented.
        """
        pass

    @staticmethod
    def load_changes_created_by_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return Change.query.filter_by(created_by=username).all()

    @staticmethod
    def load_changes_assigned_to_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return Change.query.filter_by(taken_by=username).all()

    @staticmethod
    def load_assigned_changes() -> None:
        return Change.query.filter(Change.taken_by != None).all()

    @staticmethod
    def load_unassigned_changes() -> None:
        return Change.query.filter(Change.taken_by == None).all()

    @classmethod
    def assign_change_to_user(cls, change_id: int, taken_by: str) -> None:
        user = UserController.load_by_username(username=taken_by)
        if not user:
            raise ObjectNotFoundException("User not found")
        change = cls.load_by_id(change_id)
        if not change:
            raise ObjectNotFoundException("Change not found")
        change.assign_user(
            taken_by=taken_by
        )

    @classmethod
    def relate_incident_to_change(cls, incident_id: int, change_id: int) -> None:
        incident = IncidentController.load_by_id(incident_id)
        if not incident:
            raise ObjectNotFoundException(object_name="Incident", object_id=incident_id)
        change = cls.load_by_id(change_id)
        if not change:
            raise ObjectNotFoundException(object_name="Change", object_id=change_id)
        change.incidents.append(incident)


    @classmethod
    def relate_problem_to_change(cls, problem_id: int, change_id: int) -> None:
        problem = ProblemController.load_by_id(problem_id)
        if not problem:
            raise ObjectNotFoundException(object_name="Problem", object_id=problem_id)
        change = cls.load_by_id(change_id)
        if not change:
            raise ObjectNotFoundException(object_name="Change", object_id=change_id)
        change.problems.append(problem)

    @classmethod
    def add_incidents(cls, **kwargs):
        incident_ids = kwargs.get("hardware_configuration_items", [])
        incidents = [
            IncidentController.load_by_id(incident_id) for incident_id in incident_ids
        ]

        kwargs["incidents"] = incidents
        return kwargs

    @classmethod
    def add_problems(cls, **kwargs):
        problem_ids = kwargs.get("problems", [])
        problems = [
            ProblemController.load_by_id(id) for id in problem_ids
        ]

        kwargs["problems"] = problems
        return kwargs
