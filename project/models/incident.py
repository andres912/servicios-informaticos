from project import db
from project.models.base_model import BaseModel, NullBaseModel

class Incident(BaseModel):
    __tablename__ = "incident"
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def _update(self, title: str, description: str) -> None:
        if title:
            self.title = title
        if description:
            self.description = description


class NullIncident(NullBaseModel, Incident):
    __abstract__ = True
