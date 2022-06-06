from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.solvable import Solvable
from project.models.status import *


class Problem(Solvable):
    __tablename__ = "problem"
    incidents = db.relationship("Incident", secondary="incident_problem")
    impact = db.Column(db.String(20))
    cause = db.Column(db.String(1000))
    solution = db.Column(db.String(1000))

    def __init__(
        self,
        incidents: list = [],
        impact: str = IMPACT_MEDIUM,
        cause: str = "",
        solution: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.verify_incidents(incidents)
        self.incidents = incidents
        self.impact = impact
        self.cause = cause
        self.solution = solution

    def _update(
        self,
        title: str = None,
        description: str = None,
        priority: str = None,
        status: str = None,
        taken_by: str = None,
        impact: str = None,
        cause: str = None,
        solution: str = None,
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
        if impact:
            self.impact = impact
        if cause:
            self.cause = cause
        if solution:
            self.solution = solution

    def change_status(self, status: str) -> None:
        self._update(self, status=status)

    def change_priority(self, priority: str) -> None:
        self._update(self, priority=priority)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)

    def verify_incidents(self, incidents: list) -> None:
        if not incidents:
            raise ObjectCreationException(
                object="Problem", cause="No incidents provided"
            )


class NullProblem(NullBaseModel, Problem):
    __abstract__ = True
