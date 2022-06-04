from typing import Callable
from marshmallow import pre_load, post_load, post_dump, pre_dump
from marshmallow_sqlalchemy import fields
from project import marshmallow
from project.models.base_model import BaseModel
from project.models.configuration_item.configuration_item import ConfigurationItem
from project.models.configuration_item.hardware_configuration_item import (
    HardwareConfigurationItem,
)
from project.models.configuration_item.sla_configuration_item import (
    SLAConfigurationItem,
)
from project.models.configuration_item.software_configuration_item import (
    SoftwareConfigurationItem,
)
from project.models.enableable_object import EnableableObject
from project.models.incident import Incident
from project.models.role import Role
from project.models.user import User

DATE_FORMAT = "%d/%m/%Y"


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
        fields = BaseModelSchema.Meta.fields + (
            "description",
            "priority",
            "status",
            "created_by",
            "taken_by",
            "hardware_configuration_items",
            "software_configuration_items",
            "sla_configuration_items",

            "is_blocked"
        )
        model = Incident
        include_relationships = True
        load_instance = True

    hardware_configuration_items = fields.Nested(
        "HardwareConfigurationItemSchema",
        many=True,
        only={"name", "description", "type"},
    )
    software_configuration_items = fields.Nested(
        "SoftwareConfigurationItemSchema",
        many=True,
        only={"name", "description", "type"},
    )
    sla_configuration_items = fields.Nested(
        "SLAConfigurationItemSchema",
        many=True,
        only={"name", "description", "service_type"},
    )

class AlternativeIncidentSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "description",
            "priority",
            "status",
            "created_by",
            "taken_by",
            "configuration_items",
            "is_blocked"
        )
        model = Incident
        include_relationships = True
        load_instance = True

    configuration_items = fields.fields.Method("get_configuration_items")

    def get_configuration_items(self, obj: Incident) -> list:
        return [
            {"id": item.id, "name": item.name, "type": item.item_class}
            for item in obj.hardware_configuration_items
            + obj.software_configuration_items
            + obj.sla_configuration_items
        ]



class ProblemSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "description",
            "priority",
            "status",
            "created_by",
            "taken_by",
            "impact",
            "cause",
            "solution",
            "incidents",
        )
        model = Incident
        include_relationships = True
        load_instance = True


    incidents = fields.Nested(
        "IncidentSchema", many=True, only={"id", "description", "status", "priority"}
    )



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


class ConfigurationItemSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "name",
            "description",
            "version",
            "item_family_id",
            "item_class"

        )
        include_relationships = True
        load_instance = True
    versions = fields.fields.Method("get_versions")

    def get_versions(self, obj: ConfigurationItem) -> list:
        return [
            {"id": version.id, "version": version.version, "name": version.name, "description": version.description}
            for version in obj.get_versions() if version.id != obj.id
        ]


class HardwareConfigurationItemSchema(ConfigurationItemSchema):
    class Meta:
        fields = ConfigurationItemSchema.Meta.fields + (
            "type",
            "manufacturer",
            "serial_number",
            "price",
            "purchase_date",
            "versions"
        )
        model = HardwareConfigurationItem
        include_relationships = True
        load_instance = True
    purchase_date = fields.fields.DateTime(format=DATE_FORMAT)


class SoftwareConfigurationItemSchema(ConfigurationItemSchema):
    class Meta:
        fields = ConfigurationItemSchema.Meta.fields + (
            "type",
            "provider",
            "software_version",
        )
        model = SoftwareConfigurationItem
        include_relationships = True
        load_instance = True


class SLAConfigurationItemSchema(ConfigurationItemSchema):
    class Meta:
        fields = ConfigurationItemSchema.Meta.fields + (
            "service_type",
            "service_manager",
            "client",
            "starting_date",
            "ending_date",
            "measurement_unit",
            "measurement_value",
            "is_crucial",
        )
        model = SLAConfigurationItem
        include_relationships = True
        load_instance = True

    starting_date = fields.fields.DateTime(format=DATE_FORMAT)
    ending_date = fields.fields.DateTime(format=DATE_FORMAT)
