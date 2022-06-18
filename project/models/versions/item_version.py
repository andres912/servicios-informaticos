from datetime import datetime
from imp import acquire_lock
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

    def __init__(
        self,
        item_id,
        name: str,
        description: str,
        version_number: int = 1,
        
    ):
        super().__init__()
        self.name = name
        self.description = description
        self.version_number = version_number
        self.item_id = item_id

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
