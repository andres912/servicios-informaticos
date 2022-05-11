from datetime import datetime
from imp import acquire_lock
from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.priority import *
from project.models.status import *


class ConfigurationItem(BaseModel):
    __abstract__ = True

    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable=False)
    version = db.Column(db.SmallInteger, default=1, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        name: str,
        description: str,
        item_id: int = None, # not the same as id, it's used to track changes and versions of the item
        version: int = 1
    ):
        super().__init__()
        self.item_id = item_id if item_id else self.id
        self.name = name
        self.description = description
        self.version = version

    def _update(
        self,
        name: str = None,
        description: str = None,
        item_id: int = None,
        version: str = None,

    ) -> None:
        if name:
            self.name = name
        if description:
            self.description = description
        if item_id:
            self.item_id = item_id
        if version:
            self.version = version

    def change_status(self, status: str) -> None:
        self._update(self, status=status)

    def change_priority(self, priority: str) -> None:
        self._update(self, priority=priority)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)


class NullConfigurationItem(NullBaseModel, ConfigurationItem):
    __abstract__ = True
