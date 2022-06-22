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
from project.models.problem import Problem
from project.models.role import Role
from project.models.user import User
from project.models.change import Change
from project.models.known_error import KnownError
from project.models.versions.hardware_item_version import HardwareItemVersion
from project.models.versions.item_version import ItemVersion
from project.models.versions.sla_item_version import SLAItemVersion
from project.models.versions.software_item_version import SoftwareItemVersion
from project.models.versions.known_error_version import KnownErrorVersion

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M"


class BaseModelSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "created_at", "updated_at", "is_deleted")
        model = Incident
        include_relationships = True
        load_instance = True

    created_at = fields.fields.DateTime(format=DATE_FORMAT)
    updated_at = fields.fields.DateTime(format=DATE_FORMAT)


class SolvableSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "description",
            "priority",
            "status",
            "created_by",
            "taken_by",
            "is_blocked",
            "comments",
        )
        include_relationships = True
        load_instance = True

    comments = fields.Nested("CommentSchema", many=True)


class IncidentSchema(SolvableSchema):
    class Meta:
        fields = SolvableSchema.Meta.fields + (
            "hardware_configuration_items",
            "software_configuration_items",
            "sla_configuration_items",
        )
        model = Incident
        include_relationships = True
        load_instance = True

    hardware_configuration_items = fields.Nested(
        "HardwareConfigurationItemSchema",
        many=True,
        exclude=["versions"]
    )
    software_configuration_items = fields.Nested(
        "SoftwareConfigurationItemSchema",
        many=True,
        exclude=["versions"]
    )
    sla_configuration_items = fields.Nested(
        "SLAConfigurationItemSchema",
        many=True,
        exclude=["versions"]
    )


class AlternativeIncidentSchema(SolvableSchema):
    class Meta:
        fields = SolvableSchema.Meta.fields + ("configuration_items",)
        model = Incident
        include_relationships = True
        load_instance = True

    configuration_items = fields.fields.Method("get_configuration_items")

    def get_configuration_items(self, obj: Incident) -> list:
        return [
            {"id": item.id, "name": item.current_version.name, "type": item.item_type}
            for item in obj.hardware_configuration_items
            + obj.software_configuration_items
            + obj.sla_configuration_items
        ]


class ProblemSchema(SolvableSchema):
    class Meta:
        fields = SolvableSchema.Meta.fields + ("incidents", "impact", "cause")
        model = Problem
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


class ItemVersionSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "name",
            "description",
            "version_number",
            "is_draft",
            "change_id"
        )
        include_relationships = False
        load_instance = True


class HardwareItemVersionSchema(ItemVersionSchema):
    class Meta:
        fields = ItemVersionSchema.Meta.fields + (
            "type",
            "manufacturer",
            "serial_number",
            "price",
            "purchase_date",
        )
        model = HardwareItemVersion
        include_relationships = False
        load_instance = True

    purchase_date = fields.fields.DateTime(format=DATE_FORMAT)


class SoftwareItemVersionSchema(ItemVersionSchema):
    class Meta:
        fields = ItemVersionSchema.Meta.fields + (
            "type",
            "provider",
            "software_version",
        )
        model = SoftwareItemVersion
        include_relationships = True
        load_instance = True


class SLAItemVersionSchema(ItemVersionSchema):
    class Meta:
        fields = ItemVersionSchema.Meta.fields + (
            "service_type",
            "service_manager",
            "client",
            "starting_date",
            "ending_date",
            "measurement_unit",
            "measurement_value",
            "is_crucial",
            "draft"
        )
        model = SLAItemVersion
        include_relationships = True
        load_instance = True

    starting_date = fields.fields.DateTime(format=DATE_FORMAT)
    ending_date = fields.fields.DateTime(format=DATE_FORMAT)


class DraftSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "name",
            "description",
            "version_number",
            "is_draft",
            "change_id",
            "id"
        )
        include_relationships = False
        load_instance = True

    id = fields.fields.Method("get_id")

    def get_id(self, obj: ItemVersion) -> int:
        return obj.item_id


class SLADraftSchema(DraftSchema):
    class Meta:
        fields = ItemVersionSchema.Meta.fields + (
            "service_type",
            "service_manager",
            "client",
            "starting_date",
            "ending_date",
            "measurement_unit",
            "measurement_value",
            "is_crucial",
        )
        model = SLAItemVersion
        include_relationships = True
        load_instance = True

    starting_date = fields.fields.DateTime(format=DATE_FORMAT)
    ending_date = fields.fields.DateTime(format=DATE_FORMAT)


class HardwareItemVersionSchema(ItemVersionSchema):
    class Meta:
        fields = ItemVersionSchema.Meta.fields + (
            "type",
            "manufacturer",
            "serial_number",
            "price",
            "purchase_date",
        )
        model = HardwareItemVersion
        include_relationships = False
        load_instance = True

    purchase_date = fields.fields.DateTime(format=DATE_FORMAT)


class SoftwareItemVersionSchema(ItemVersionSchema):
    class Meta:
        fields = ItemVersionSchema.Meta.fields + (
            "type",
            "provider",
            "software_version",
        )
        model = SoftwareItemVersion
        include_relationships = True
        load_instance = True


class ReducedConfigurationItemSchema(BaseModelSchema):
    class Meta:
        fields = ("name",)
        include_relationships = True
        load_instance = True
    
    name = fields.fields.Method("get_name")

    def get_name(self, obj: ConfigurationItem) -> str:
        return obj.current_version.name

class ConfigurationItemSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "last_version",
            "item_type",
            "draft_change_id",
            "draft_id",
            "current_version_id"
        )
        include_relationships = True
        load_instance = True

    draft_change_id = fields.fields.Method("get_draft_change_id")
    draft = fields.Nested(DraftSchema, dump_only=True)

    def get_draft_change_id(self, obj: ConfigurationItem) -> str:
        draft = obj.draft
        return draft.change_id if draft else None
    
    @post_dump(pass_many=True)
    def rearrange_info(self, data, many, **kwargs):
        """
        Needy to use versions as a list object when dumping ConfigurationItem into json.
        """
        def remove_current_version_and_draft_from_versions(item_data):
            if not "versions" in item_data:
                return
            versions = item_data["versions"][:]
            for version in versions:
                if version["id"] == item_data["current_version_id"] or version["is_draft"] == True:
                    item_data["versions"].remove(version)

        def extract_version_info(item_data, attach_to_draft=False):
            field_to_attach = "current_version" if not attach_to_draft else "draft"
            if not item_data[field_to_attach]:
                del item_data[field_to_attach]
                return
            for key in item_data[field_to_attach]:
                if key == "id":
                    continue
                elif key == "version_number" and not attach_to_draft:
                    item_data["current_version_number"] = item_data["current_version"][key]
                else:
                    item_data[key] = item_data[field_to_attach][key]
            del item_data[field_to_attach]

        # if current_version is excluded, the item is attached to its draft
        if many:
            for item_data in data:
                attach_to_draft = item_data["draft_id"] != None and "current_version" in self.exclude
                extract_version_info(item_data, attach_to_draft)
                remove_current_version_and_draft_from_versions(item_data)
        else:
            attach_to_draft = data["draft_id"] != None and "current_version" in self.exclude
            extract_version_info(data, attach_to_draft)
            remove_current_version_and_draft_from_versions(data)
        return data


class HardwareConfigurationItemSchema(ConfigurationItemSchema):
    class Meta:
        fields = ConfigurationItemSchema.Meta.fields + (
            "current_version",
            "draft",
            "versions"
        )
        model = HardwareConfigurationItem
        include_relationships = True
        load_instance = True

    purchase_date = fields.fields.DateTime(format=DATE_FORMAT)
    current_version = fields.Nested("HardwareItemVersionSchema")
    draft = fields.Nested("HardwareItemVersionSchema")
    versions = fields.Nested("ItemVersionSchema", many=True, only=("id", "version_number", "name", "is_draft"))


class SoftwareConfigurationItemSchema(ConfigurationItemSchema):
    class Meta:
        fields = ConfigurationItemSchema.Meta.fields + (
            "current_version",
            "draft",
            "versions"
        )
        model = SoftwareConfigurationItem
        include_relationships = True
        load_instance = True

    current_version = fields.Nested("SoftwareItemVersionSchema")
    draft = fields.Nested("SoftwareItemVersionSchema")
    versions = fields.Nested("ItemVersionSchema", many=True, only=("id", "version_number", "name", "is_draft"))
    

class SLAConfigurationItemSchema(ConfigurationItemSchema):
    class Meta:
        fields = ConfigurationItemSchema.Meta.fields + (
            "current_version",
            "draft",
            "versions"
        )
        model = SLAConfigurationItem
        include_relationships = True
        load_instance = True
    
    current_version = fields.Nested("SLAItemVersionSchema")
    draft = fields.Nested("SLAItemVersionSchema")
    versions = fields.Nested("ItemVersionSchema", many=True, only=("id", "version_number", "name", "is_draft"))


class ChangeSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "description",
            "priority",
            "status",
            "created_by",
            "taken_by",
            "incidents",
            "problems",
            "hardware_configuration_items",
            "software_configuration_items",
            "sla_configuration_items",
        )
        model = Change
        include_relationships = True
        load_instance = True
    
    hardware_configuration_items = fields.Nested(
        "HardwareConfigurationItemSchema",
        many=True,
        exclude=["versions"]
    )
    software_configuration_items = fields.Nested(
        "SoftwareConfigurationItemSchema",
        many=True,
        exclude=["versions"]
    )
    sla_configuration_items = fields.Nested(
        "SLAConfigurationItemSchema",
        many=True,
        exclude=["versions"]
    )

    incidents = fields.Nested(
        "IncidentSchema", many=True, only={"id", "description", "status", "priority"}
    )

    problems = fields.Nested(
        "ProblemSchema", many=True, only={"id", "description", "status", "priority"}
    )


class KnownErrorSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "current_version",
            "current_version_id",
            "versions",
            "incidents",
        )
        model = KnownError
        include_relationships = True
        load_instance = True

    incidents = fields.Nested(
        "IncidentSchema", many=True, only={"id", "description", "status", "priority"}
    )

    current_version = fields.Nested("KnownErrorVersionSchema")
    versions = fields.Nested("KnownErrorVersionSchema", many=True)

    @post_dump(pass_many=True)
    def rearrange_info(self, data, many, **kwargs):
        """
        Needy to use versions as a list object when dumping KnownError into json.
        """
        def remove_current_version_from_versions(item_data):
            if not "versions" in item_data:
                return
            versions = item_data["versions"][:]
            for version in versions:
                if version["id"] == item_data["current_version_id"]:
                    item_data["versions"].remove(version)

        def extract_version_info(item_data):
            field_to_attach = "current_version"
            if not item_data[field_to_attach]:
                del item_data[field_to_attach]
                return
            for key in item_data[field_to_attach]:
                if key == "id":
                    continue
                elif key == "version_number":
                    item_data["current_version_number"] = item_data["current_version"][key]
                else:
                    item_data[key] = item_data[field_to_attach][key]
            del item_data[field_to_attach]

        #todo ver la importancia de esta parte
        # if current_version is excluded, the item is attached to its draft
        if many:
            for item_data in data:
                extract_version_info(item_data)
                remove_current_version_from_versions(item_data)
        else:
            extract_version_info(data)
            remove_current_version_from_versions(data)
        return data

class KnownErrorVersionSchema(BaseModelSchema):
    class Meta:
        fields = BaseModelSchema.Meta.fields + (
            "description",
            "solution",
            "version_number",
            "created_by"
        )
        model = KnownErrorVersion
        include_relationships = False
        load_instance = True


class CommentSchema(BaseModelSchema):
    class Meta:
        fields = ("created_at", "created_by", "text")

    created_at = fields.fields.DateTime(format=DATETIME_FORMAT)
