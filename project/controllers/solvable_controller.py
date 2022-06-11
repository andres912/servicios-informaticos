from project.controllers.base_controller import BaseController
from project.controllers.user_controller import UserController
from project.models.exceptions import MissingFieldsException, ObjectNotFoundException
from project.models.incident import Incident, NullIncident
from project.models.solvable import NullSolvable, Solvable
from project.models.status import STATUS_SOLVED
from project import db


class SolvableController(BaseController):
    object_class = Solvable
    null_object_class = NullSolvable

    @staticmethod
    def _verify_relations(incident: Incident) -> None:
        """
        Must be implemented.
        """
        pass

    @staticmethod
    def load_created_by_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return Incident.query.filter_by(created_by=username).all()

    @staticmethod
    def load_assigned_to_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return Incident.query.filter_by(taken_by=username).all()

    @classmethod
    def assign_to_user(cls, object_id: int, taken_by: str) -> None:
        user = UserController.load_by_username(username=taken_by)
        if not user:
            raise ObjectNotFoundException("User not found")
        object = cls.load_by_id(object_id)
        if not object:
            raise ObjectNotFoundException(f"{cls.object_class.__name__} not found")
        object.assign_user(
            taken_by=taken_by
        )

    @classmethod
    def add_comment_to_solvable(cls, solvable_id: int, comment_message: str, created_by: str) -> None:
        if not solvable_id or not comment_message or not created_by:
            return
        
        comment = cls.comment_class(text=comment_message, object_id=solvable_id, created_by=created_by)
        db.session.add(comment)
        db.session.commit()

    @classmethod
    def load_solved(cls) -> None:
        return cls.object_class.query.filter(cls.object_class.status == STATUS_SOLVED).all()

    @classmethod
    def load_assigned(cls) -> None:
        return cls.object_class.query.filter(cls.object_class.taken_by != None).all()

    @classmethod
    def load_unassigned(cls) -> None:
        return cls.object_class.query.filter(cls.object_class.taken_by == None).all()

    @classmethod
    def load_taken_by_user(cls, username: str) -> None:
        return cls.object_class.query.filter(cls.object_class.taken_by == username).all()

    @classmethod
    def load_by_name(cls, object_name: str) -> None:
        return cls.object_class.query.filter(cls.object_class.name == object_name).first()

    @classmethod
    def load_by_description(cls, description: str) -> None:
        return cls.object_class.query.filter(cls.object_class.description == description).first()

