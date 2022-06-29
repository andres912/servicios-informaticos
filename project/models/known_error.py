from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.solvable import Solvable
from project.models.status import *
from sqlalchemy import ForeignKey
from project.models.association_tables.incident_known_error import IncidentKnownError
from project.models.versions.known_error_version import KnownErrorVersion


class KnownError(BaseModel):
    __tablename__ = "known_error"
    incidents = db.relationship("Incident", secondary="incident_known_error")
    last_version = db.Column(db.SmallInteger, nullable=False)

    current_version_id = db.Column(
        db.Integer, ForeignKey("known_error_version.id"), nullable=True
    )

    versions = db.relationship(
        "KnownErrorVersion",
        foreign_keys="KnownErrorVersion.known_error_id",
        cascade="all, delete-orphan",
    )

    current_version = db.relationship(
        "KnownErrorVersion", foreign_keys=[current_version_id]
    )

    def __init__(
        self,
        current_version_id: int = None,
        incidents: list = [],
        **kwargs
    ):
        self.incidents = incidents
        self.current_version_id = current_version_id
        self.last_version = 1
        super().__init__(**kwargs)

    def _update(
        self,
        title: str = None,
        description: str = None,
        solution: str = None,
        taken_by: str = None,
        **kwargs
    ) -> None:
        if title:
            self.title = title
        if description:
            self.description = description
        if solution:
            self.solution = solution
        if taken_by:
            self.taken_by = taken_by
        return self.current_version.update(**kwargs)



    def verify_incidents(self, incidents: list) -> None:
        if not incidents:
            raise ObjectCreationException(
                object="KnownError", cause="Requires at least 1 incident"
            )

    def set_current_version(self, version_id: int):
        self.current_version_id = version_id

class NullKnownError(NullBaseModel, KnownError):
    __abstract__ = True
