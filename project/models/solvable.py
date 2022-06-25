from sqlalchemy import ForeignKey
from project import db
from project.db_types.list_type import MutableList
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.status import *
from project.models.association_tables.configuration_item_incident import HardwareConfigurationItemIncident
from project.models.association_tables.configuration_item_incident import SoftwareConfigurationItemIncident
from project.models.association_tables.configuration_item_incident import SLAConfigurationItemIncident
from sqlalchemy.ext.declarative import declared_attr


class Solvable(BaseModel):
    __abstract__ = True
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    is_blocked = db.Column(db.Boolean, default=False)

    @declared_attr
    def created_by(cls):
        return db.Column(db.String(30), ForeignKey("user.username"))

    @declared_attr
    def taken_by(cls):
        return db.Column(db.Integer, ForeignKey("user.username"))


    def __init__(
        self,
        description: str,
        priority: str = PRIORITY_MEDIUM,
        created_by: str = ""
    ):
        self.description = description
        self.priority = priority
        self.created_by = created_by
        self.status = STATUS_PENDING
        self.taken_by = None
        self.is_blocked = False


    def _update(self,
                title: str = None,
                description: str = None,
                priority: str = None,
                status: str = None,
                taken_by: str = None,
                is_blocked: bool = None) -> None:

        if title:
            self.title = title
        if description:
            self.description = description
        if priority:
            self.priority = priority
        if status:
            self.status = status
        if taken_by:
            self.taken_by = taken_by

        if is_blocked != None:
            self.is_blocked = is_blocked


    def change_status(self, status: str) -> None:
        self._update(self, status=status)

    def change_priority(self, priority: str) -> None:
        self._update(self, priority=priority)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)

    def verify_items(self, hardware_configuration_items: list, software_configuration_items: list, sla_configuration_items: list) -> None:
        if not hardware_configuration_items and not software_configuration_items and not sla_configuration_items:
            raise ObjectCreationException(object="Incident", cause="No configuration items provided")

    def add_comment(self, comment: str) -> None:
        if self.comments == None:
            self.comments = [comment]
        else:
            self.comments.append(comment)

class NullSolvable(NullBaseModel, Solvable):
    __abstract__ = True
