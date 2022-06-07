from project.controllers.base_controller import BaseController
from project.controllers.incident_controller import IncidentController
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.change import Change, NullChange


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


