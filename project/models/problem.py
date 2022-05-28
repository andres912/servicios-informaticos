from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.status import *
from project.models.association_tables.configuration_item_incident import HardwareConfigurationItemIncident
from project.models.association_tables.configuration_item_incident import SoftwareConfigurationItemIncident
from project.models.association_tables.configuration_item_incident import SLAConfigurationItemIncident


class Problem(BaseModel):
    __tablename__ = "problem"
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20))
    created_by = db.Column(db.String(30), db.ForeignKey("user.username"))
    taken_by = db.Column(db.String(30), db.ForeignKey("user.username"))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    incidents = db.relationship("Incident", secondary="incident_problem")
    impact = db.Column(db.String(20))
    cause = db.Column(db.String(1000))
    solution = db.Column(db.String(1000))

    def __init__(
        self,
        description: str,
        priority: str = PRIORITY_MEDIUM,
        created_by: str = "",
        incidents: list = [],
        impact: str = IMPACT_MEDIUM,
        cause: str = "",
        solution: str = "",
    ):
        self.verify_incidents(incidents)
        self.description = description
        self.priority = priority
        self.created_by = created_by
        self.status = STATUS_PENDING
        self.taken_by = None
        self.impact = impact
        self.cause = cause
        self.solution = solution


    def _update(self, title: str = None, description: str = None, priority: str = None, status: str = None, taken_by: str = None, impact: str = None, cause: str = None, solution: str = None) -> None:
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
            raise ObjectCreationException(object="Problem", cause="No incidents provided")

class NullProblem(NullBaseModel, Problem):
    __abstract__ = True
