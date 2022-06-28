from datetime import datetime
from imp import acquire_lock

from sqlalchemy import ForeignKey
from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.status import *
from sqlalchemy.ext.declarative import declared_attr

class ItemVersion(BaseModel):
    __abstract__ = True

    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable=False)
    version_number = db.Column(db.SmallInteger, default=1, nullable=False)
    is_draft = db.Column(db.Boolean, default=False, nullable=False)
    is_restoring_draft = db.Column(db.Boolean, default=False, nullable=True)
    restore_version_id = db.Column(db.Integer, default=None, nullable = True)

    @declared_attr
    def change_id(cls):
        return db.Column(db.Integer, ForeignKey("change.id"), nullable=True)

    def __init__(
        self,
        item_id,
        name: str,
        description: str,
        version_number: int = 1,
        is_draft: bool = False,
        change_id: int = None,
        is_restoring_draft: bool = False,
        restore_version_id: int = None,
        
    ):
        super().__init__()
        self.name = name
        self.description = description
        self.version_number = version_number
        self.item_id = item_id
        self.is_draft = is_draft
        self.change_id = change_id
        self.is_restoring_draft = is_restoring_draft
        self.restore_version_id = restore_version_id

    def _update(
        self,
        name: str = None,
        description: str = None,

    ) -> None:
        if name:
            self.name = name
        if description:
            self.description = description


class NullConfigurationItem(NullBaseModel, ItemVersion):
    __abstract__ = True
