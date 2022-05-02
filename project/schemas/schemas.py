from typing import Callable
from marshmallow import pre_load, post_load, post_dump, pre_dump
from marshmallow_sqlalchemy import fields
from project import marshmallow
from project.models.base_model import BaseModel
from project.models.enableable_object import EnableableObject
from project.models.incident import Incident
from project.models.role import Role
from project.models.user import User

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

class RoleSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + ("name", "permissions")
        model = Role
        include_relationships = True
        load_instance = True

    @post_dump(pass_many=True)
    def permission_as_list(self, data, many, **kwargs):
        """
        Needy to use permissions as a list object when dumping Role into json.
        """

        def str_to_list(x: str) -> list:
            """
            Given an string representation of a list returns a list.
            example:
                str_to_list("['this', 'is', 'an', 'example']") -> ['this', 'is', 'an', 'example']
            """
            if x == "[]":
                return []
            return x[2:-2].split("', '")

        try:
            if many:
                for role in data:
                    role["permissions"] = str_to_list(role["permissions"])
            else:
                data["permissions"] = str_to_list(data["permissions"])
        except KeyError:
            pass
        return data

class UserSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "username",
            "email",
            "registered_on",
            "role",
            "role_id",
            "name",
            "lastname",
            "is_enabled",
            "last_activity_at",
            "is_visible",
        )
        model = User
        include_relationships = True
        load_instance = True

    role = fields.Nested(RoleSchema(only=("id", "name")), dump_only=True)

