from typing import Any, List

from project.controllers.base_controller import BaseController, ValidationError
from project.models.role import Role, NullRole


def get_validation_error_message(obj_name: str, parameter: str, comment: str, comment_es: str, value: Any = None):
    return {
        "error": f"invalid_{obj_name}",
        "parameter": parameter,
        "value": value,
        "description": f"The given {parameter} {comment}",
        "description_es": f"{comment_es}",
    }


class RoleController(BaseController):
    object_class = Role
    null_object_class = NullRole

    @staticmethod
    def _verify_relations(new_role: Role) -> None:
        """
        No verifications needed.
        """
        pass

    @classmethod
    def load_all(cls) -> List[Role]:
        """
        Returns all Role objects, filtered by not deleted.
        """
        roles = cls.object_class.query.filter_by(is_deleted=False).all()
        return roles

    @classmethod
    def verify_existent_role_name(cls, name: str, id: int = None):
        """
        Receives a role name and a role id.
        Verifies its matching and raises an error if they do as the Role already exists.
        Returns True otherwise.
        """
        role_by_name = Role.query.filter_by(name=name).first()
        role_by_id = Role.query.filter_by(id=id).first()
        if role_by_name and role_by_id != role_by_name:
            raise ValidationError(
                message=[
                    get_validation_error_message("role", "rolename", "already exists", "El rol ya existe", value=name)
                ]
            )

        return True

    @classmethod
    def load_updated(cls, id: int, **kwargs):
        """
        Receives role data and updates the role with it.
        If the role exists:
            it updates the data if needed
        Otherwise:
            it creates a new role

        Returns: role
        """
        if "name" in kwargs:
            RoleController.verify_existent_role_name(kwargs["name"], id)
        return super().load_updated(id, **kwargs)

    @classmethod
    def create(cls, name, permissions) -> Role:
        """
        Receives a name and permissions and creates a Role object.
        Returns the new Role object.
        """
        # Verify existent role
        RoleController.verify_existent_role_name(name)
        new_role = Role(name, permissions)
        return new_role
