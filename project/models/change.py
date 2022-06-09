from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.solvable import Solvable
from project.models.status import *


class Change(Solvable):
    __tablename__ = "change"
    incidents = db.relationship("Incident", secondary="incident_change")
    problems = db.relationship("Problem", secondary="problem_change")

    def __init__(self, incidents: list = [], problems: list = [], **kwargs):
        self.incidents = incidents
        self.problems = problems
        super().__init__(**kwargs)

    def _update(
        self,
        title: str = None,
        description: str = None,
        priority: str = None,
        status: str = None,
        taken_by: str = None,
    ) -> None:
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
    
    def verify_problems_incidents(self, incidents: list, problems: list) -> None:
        if not problems and not incidents:
            raise ObjectCreationException(
                object="Change", cause="Requires atleast 1 incident OR problem"
            )



class NullChange(NullBaseModel, Change):
    __abstract__ = True
