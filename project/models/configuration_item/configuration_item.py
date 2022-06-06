from datetime import datetime
from imp import acquire_lock
from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.priority import *
from project.models.status import *
from project.models.association_tables.configuration_item_incident import *

class ConfigurationItem(BaseModel):
    __abstract__ = True

    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable=False)
    version = db.Column(db.SmallInteger, default=1, nullable=False)
    item_family_id = db.Column(db.Integer, nullable=True)
    item_class = db.Column(db.String(20), nullable=False)
    is_current_version = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(
        self,
        name: str,
        description: str,
        item_class: str,
        item_family_id: int = None, # not the same as id, it's used to track changes and versions of the item
        version: int = 1,
        is_current_version: bool = True,
    ):
        super().__init__()
        if item_family_id:
            self.item_family_id = item_family_id
        self.name = name
        self.description = description
        self.version = version
        self.item_class = item_class
        self.is_current_version = is_current_version

    def _update(
        self,
        name: str = None,
        description: str = None,
        item_family_id: int = None,
        version: str = None,

    ) -> None:
        if name:
            self.name = name
        if description:
            self.description = description
        if item_family_id:
            self.item_family_id = item_family_id
        if version:
            self.version = version

    def get_versions(self):
        if not self.item_family_id:
            return []
        return self.query.filter_by(item_family_id=self.item_family_id).all()


class NullConfigurationItem(NullBaseModel, ConfigurationItem):
    __abstract__ = True
