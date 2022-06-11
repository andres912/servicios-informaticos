from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.solvable import Solvable
from project.models.status import *


class KnownError(Solvable):
    __tablename__ = "know_error"
    #incidents = db.relationship("Incident", secondary="incident_known_error") #! not working

    def __init__(self, incidents: list = [], **kwargs):
        self.incidents = incidents
        super().__init__(**kwargs)

    def _update(
        self,
        title: str = None,
        description: str = None,
        solution: str = None,
        taken_by: str = None,
    ) -> None:
        if title:
            self.title = title
        if description:
            self.description = description
        if solution:
            self.solution = solution
        if taken_by:
            self.taken_by = taken_by

    def change_solution(self, solution: str) -> None:
        self._update(self, solution=solution)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)

    def verify_incidents(self, incidents: list) -> None:
        if not incidents:
            raise ObjectCreationException(
                object="KnownError", cause="Requires at least 1 incident"
            )

class NullKnownError(NullBaseModel, KnownError):
    __abstract__ = True
