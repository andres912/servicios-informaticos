from project.controllers.base_controller import BaseController
from project.controllers.incident_controller import IncidentController
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.known_error import KnownError, NullKnownError
from project.models.association_tables.incident_known_error import IncidentKnownError

from project.controllers.user_controller import UserController


class KnownErrorController(BaseController):
    object_class = KnownError
    null_object_class = NullKnownError

    @staticmethod
    def _verify_relations(known_error: KnownError) -> None:
        """
        Must be implemented.
        """
        pass

    @staticmethod
    def load_known_errors_created_by_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return KnownError.query.filter_by(created_by=username).all()

    @staticmethod
    def load_known_errors_assigned_to_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return KnownError.query.filter_by(taken_by=username).all()

    @staticmethod
    def load_assigned_known_errors() -> None:
        return KnownError.query.filter(KnownError.taken_by != None).all()

    @staticmethod
    def load_unassigned_known_errors() -> None:
        return KnownError.query.filter(KnownError.taken_by == None).all()

    @classmethod
    def assign_known_errors_to_user(cls, error_id: int, taken_by: str) -> None:
        user = UserController.load_by_username(username=taken_by)
        if not user:
            raise ObjectNotFoundException("User not found")
        error = cls.load_by_id(error_id)
        if not error:
            raise ObjectNotFoundException("Known error not found")
        error.assign_user(
            taken_by=taken_by
        )
