from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from project.models.base_model import BaseModel

IncidentProblem = Table(
    "incident_problem",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("incident_id", Integer, ForeignKey("incident.id")),
    Column("problem_id", Integer, ForeignKey("problem.id")),
)
