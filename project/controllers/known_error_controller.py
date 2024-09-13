from project.controllers.base_controller import BaseController
from project.controllers.incident_controller import IncidentController
from project.models.known_error import KnownError, NullKnownError
from project.models.association_tables.incident_known_error import IncidentKnownError
from project.models.versions.known_error_version import KnownErrorVersion
from project import db
from typing import List

from project.models.exceptions import (
    MissingFieldsException,
    ObjectNotFoundException,
    KnownErrorVersionNotFoundException,
)

from project.controllers.user_controller import UserController


class KnownErrorController(BaseController):
    object_class = KnownError
    null_object_class = NullKnownError
    object_version_class = KnownErrorVersion

    @staticmethod
    def _verify_relations(known_error: KnownError) -> None:
        """
        Must be implemented.
        """
        pass

    @classmethod
    def create(cls, **kwargs) -> KnownError:
        """
        Creates and saves KnownError object.
        """
        solution = kwargs["solution"]  # veneno
        del kwargs["solution"]  # antidoto
        created = kwargs["created_by"]  # veneno
        del kwargs["created_by"]  # antidoto
        description = kwargs["description"]  # veneno
        del kwargs["description"]  # antidoto

        known_error = cls.object_class(**kwargs)
        db.session.add(known_error)
        db.session.commit()  # necesario para tener el id

        kwargs["known_error_id"] = known_error.id
        kwargs["solution"] = solution
        kwargs["description"] = description
        kwargs["created_by"] = created
        del kwargs["incidents"]
        known_error_version = cls.object_version_class(**kwargs)
        db.session.add(known_error_version)
        db.session.commit()

        known_error.set_current_version(known_error_version.id)
        db.session.commit()

        for incident in known_error.incidents:
            cls.add_incident_to_error(known_error.id, incident.description)

        return known_error

    @classmethod
    def update(cls, known_error_id: int, **kwargs) -> KnownError:
        """
        Updates and saves KnownError object.
        """
        known_error = cls.load_by_id(known_error_id)
        if not known_error:
            raise ObjectNotFoundException(
                object_name="Known Error", object_id=known_error_id
            )
        # cls._verify_relations(known_error_id)
        known_error.update(**kwargs)
        db.session.commit()
        return known_error

    @classmethod
    def restore_known_error_version(cls, known_error_id: int, version_number: int):
        known_error = cls.load_by_id(known_error_id)
        new_version = cls.object_version_class.query.filter_by(
            known_error_id=known_error_id, version_number=version_number
        ).first()
        if not new_version:
            raise KnownErrorVersionNotFoundException(known_error_id, version_number)
        known_error.current_version_id = new_version.id
        db.session.commit()
        return known_error

    @classmethod
    def load_all(cls) -> List[KnownError]:
        """
        Returns all Model objects, filtered by not deleted.
        """
        return cls.object_class.query.filter_by(is_deleted=False).all()

    @classmethod
    def create_new_known_error_version(cls, known_error_id: int, **kwargs):
        known_error = cls.load_by_id(known_error_id)
        new_version_number = known_error.last_version + 1

        kwargs["version_number"] = new_version_number
        kwargs["known_error_id"] = known_error_id

        new_version = cls.object_version_class(**kwargs)
        db.session.add(new_version)
        db.session.commit()

        known_error.last_version = new_version_number
        known_error.set_current_version(new_version.id)
        db.session.commit()

        return known_error

    @staticmethod
    def load_known_errors_created_by_user(username: str = "") -> None:
        if not username:
            raise MissingFieldsException(missing_fields=["username"])
        return KnownError.query.filter_by(created_by=username).all()

    @classmethod
    def add_incident_to_error(cls, known_error_id: int, incident_description: str):
        incident = IncidentController.load_by_description(incident_description)
        if not incident:
            raise ObjectNotFoundException(
                object_name="Incident", object_id=incident_description
            )

        known_error = cls.load_by_id(known_error_id)
        if not known_error:
            raise ObjectNotFoundException(
                object_name="Known Error", object_id=known_error_id
            )

        current_version_number = known_error.current_version.version_number
        db.engine.execute(
            IncidentKnownError.insert(),
            incident_id=incident.id,
            known_error_id=known_error.id,
            version_used=current_version_number,
        )
        solution_used = known_error.current_version.solution
        IncidentController.add_comment_to_solvable(
            incident.id,
            f'Se utilizó la solución: "{solution_used}" para intentar resolver el incidente',
        )
        db.session.commit()
        return known_error
