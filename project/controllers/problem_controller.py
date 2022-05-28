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
from project.controllers.incident_controller import IncidentController
from project.controllers.user_controller import UserController
from project.models.association_tables.incident_problem import IncidentProblem
from project.models.exceptions import BadQueryException, ObjectNotFoundException
from project.models.problem import Problem, NullProblem


class ProblemController(BaseController):
    object_class = Problem
    null_object_class = NullProblem

    @staticmethod
    def _verify_relations(problem: Problem) -> None:
        """
        Must be implemented.
        """
        pass

    @staticmethod
    def load_problems_created_by_user(username: str = "") -> None:
        if not username:
            raise BadQueryException("Username is required.")
        return Problem.query.filter_by(created_by=username).all()

    @staticmethod
    def load_problems_assigned_to_user(username: str = "") -> None:
        if not username:
            raise BadQueryException("Username is required.")
        return Problem.query.filter_by(taken_by=username).all()

    @staticmethod
    def load_assigned_problems() -> None:
        return Problem.query.filter(Problem.taken_by != None).all()

    @staticmethod
    def load_unassigned_problems() -> None:
        return Problem.query.filter(Problem.taken_by == None).all()

    @classmethod
    def assign_problem_to_user(cls, problem_id: int, taken_by: str) -> None:
        user = UserController.load_by_username(username=taken_by)
        if not user:
            raise ObjectNotFoundException("User not found")
        problem = cls.load_by_id(problem_id)
        if not problem:
            raise ObjectNotFoundException("Problem not found")
        problem.assign_user(
            taken_by=taken_by
        )  # you don't need to save the problem again. Why? There is no why.

    @classmethod
    def relate_incident_to_problem(cls, incident_id: int, problem_id: int) -> None:
        incident = IncidentController.load_by_id(incident_id)
        if not incident:
            raise ObjectNotFoundException(object_name="Incident", object_id=incident_id)
        problem = cls.load_by_id(problem_id)
        if not problem:
            raise ObjectNotFoundException(object_name="Problem", object_id=problem_id)
        problem.incidents.append(incident)

    @classmethod
    def create(cls, **kwargs) -> Problem:
        modified_parameters = cls.add_incidents(**kwargs)
        return super().create(**modified_parameters)

    @classmethod
    def add_incidents(cls, **kwargs):
        incident_ids = kwargs.get("hardware_configuration_items", [])
        incidents = [
            IncidentController.load_by_id(incident_id) for incident_id in incident_ids
        ]

        kwargs["incidents"] = incidents
        return kwargs

