from datetime import datetime
from imp import acquire_lock
from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.status import *
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import ForeignKey

class KnownErrorVersion(BaseModel):
    __tablename__ = "known_error_version"

    description = db.Column(db.String(500), nullable=False)
    solution = db.Column(db.String(1000), nullable=False)
    version_number = db.Column(db.SmallInteger, default=1, nullable=False)
    known_error_id = db.Column(db.Integer, db.ForeignKey("known_error.id"), nullable=False)
    created_by = db.Column(db.String(30), ForeignKey("user.username"))

    def __init__(
        self,
        known_error_id,
        description: str,
        solution: str,
        created_by: str = "",
        version_number: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.description = description
        self.version_number = version_number
        self.known_error_id = known_error_id
        self.solution = solution
        self.created_by = created_by

    def _update(
        self,
        description: str = None,
        solution: str = None,
    ) -> None:
        if description:
            self.description = description
        if solution:
            self.solution = solution

class NullConfigurationItem(NullBaseModel, KnownErrorVersion):
    __abstract__ = True
