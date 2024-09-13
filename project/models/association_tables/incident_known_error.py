from sqlalchemy import SmallInteger, Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from project.models.base_model import BaseModel

IncidentKnownError = Table(
    "incident_known_error",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("incident_id", Integer, ForeignKey("incident.id")),
    Column("known_error_id", Integer, ForeignKey("known_error.id")),
    Column("version_used", SmallInteger, nullable=True, default=None),
)
