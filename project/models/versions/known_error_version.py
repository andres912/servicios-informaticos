from datetime import datetime
from imp import acquire_lock
from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.status import *
from sqlalchemy.ext.declarative import declared_attr

class KnownErrorVersion(BaseModel):
    __tablename__ = "known_error_version"

    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable=False)
    solution = db.Column(db.String(1000), nullable=False)
    version_number = db.Column(db.SmallInteger, default=1, nullable=False)
    known_error_id = db.Column(db.Integer, db.ForeignKey("known_error.id"), nullable=False)

    def __init__(
        self,
        item_id,
        name: str,
        description: str,
        solution: str,
        version_number: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.version_number = version_number
        self.item_id = item_id
        self.solution = solution

    def _update(
        self,
        name: str = None,
        description: str = None,
        solution: str = None,
    ) -> None:
        if name:
            self.name = name
        if description:
            self.description = description
        if solution:
            self.solution = solution

class NullConfigurationItem(NullBaseModel, KnownErrorVersion):
    __abstract__ = True
