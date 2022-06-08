from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from project.models.base_model import BaseModel

ProblemChange = Table(
    "problem_change",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("problem_id", Integer, ForeignKey("problem.id")),
    Column("change_id", Integer, ForeignKey("change.id")),
)
