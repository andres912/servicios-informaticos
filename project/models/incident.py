from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.priority import *
from project.models.status import *


class Incident(BaseModel):
    __tablename__ = "incident"
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20))
    created_by = db.Column(db.String(30), db.ForeignKey("user.username"))
    taken_by = db.Column(db.String(30), db.ForeignKey("user.username"))

    def __init__(
        self,
        description: str,
        priority: str = PRIORITY_MEDIUM,
        created_by: str = ""
    ):
        self.description = description
        self.priority = priority
        self.status = STATUS_PENDING
        self.created_by = created_by
        self.taken_by = None


    def _update(self, title: str = None, description: str = None, priority: str = None, status: str = None, taken_by: str = None) -> None:
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

    def change_status(self, status: str) -> None:
        self._update(self, status=status)

    def change_priority(self, priority: str) -> None:
        self._update(self, priority=priority)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)


class NullIncident(NullBaseModel, Incident):
    __abstract__ = True
