from typing import Callable
from marshmallow import pre_load, post_load, post_dump, pre_dump
from marshmallow_sqlalchemy import fields
from project import marshmallow
from project.models.base_model import BaseModel
from project.models.enableable_object import EnableableObject
from project.models.incident import Incident

DATE_FORMAT = "%d/%m/%y"


class BaseModelSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "created_at", "updated_at", "is_deleted")
        model = Incident
        include_relationships = True
        load_instance = True

    created_at = fields.fields.DateTime(format=DATE_FORMAT)
    updated_at = fields.fields.DateTime(format=DATE_FORMAT)

class IncidentSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + ("title", "description")
        model = Incident
        include_relationships = True
        load_instance = True
