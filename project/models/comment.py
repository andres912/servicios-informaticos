import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.types import PickleType
from typing import List
from project import db
from project.db_types.list_type import MutableList
from project.models.base_model import BaseModel, NullBaseModel
from project.models.permission import *
from sqlalchemy.ext.declarative import declared_attr


class Comment(BaseModel):
    """
    Class that represents a comment
    """

    __tablename__ = "comment"
    __abstract__ = True

    text = db.Column(db.String(500))
    has_link = db.Column(db.Boolean, default=False)
    link_url = db.Column(db.String(500))
    link_text = db.Column(db.String(500))

    @declared_attr
    def created_by(cls):
        return db.Column(db.String(30), ForeignKey("user.username"))

    def __init__(self, text: str, created_by: str = None):
        self.text = text
        self.created_by = created_by


class IncidentComment(Comment):

    __tablename__ = "comment_incident"

    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))

    def __init__(self, text: str, object_id: int, created_by: str = None):
        super().__init__(text, created_by)
        self.incident_id = object_id


class ProblemComment(Comment):

    __tablename__ = "comment_problem"

    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))

    def __init__(self, text: str, object_id: int, created_by: str = None):
        super().__init__(text, created_by)
        self.problem_id = object_id


class ChangeComment(Comment):

    __tablename__ = "comment_change"

    change_id = db.Column(db.Integer, db.ForeignKey("change.id"))

    def __init__(self, text: str, object_id: int, created_by: str = None):
        super().__init__(text, created_by)
        self.change_id = object_id


class HardwareItemComment(Comment):

    __tablename__ = "comment_hardware_item"

    hardware_item_id = db.Column(db.Integer, db.ForeignKey("ci_hardware.id"))

    def __init__(self, text: str, object_id: int, created_by: str = None):
        super().__init__(text, created_by)
        self.hardware_item_id = object_id


class SoftwareItemComment(Comment):

    __tablename__ = "comment_software_item"

    software_item_id = db.Column(db.Integer, db.ForeignKey("ci_software.id"))

    def __init__(self, text: str, object_id: int, created_by: str = None):
        super().__init__(text, created_by)
        self.software_item_id = object_id


class SLAItemComment(Comment):

    __tablename__ = "comment_sla_item"

    sla_item_id = db.Column(db.Integer, db.ForeignKey("ci_sla.id"))

    def __init__(self, text: str, object_id: int, created_by: str = None):
        super().__init__(text, created_by)
        self.sla_item_id = object_id
