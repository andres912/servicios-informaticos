from sqlalchemy.types import PickleType
from typing import List
from project import db
from project.db_types.list_type import MutableList
from project.models.base_model import BaseModel, NullBaseModel
from project.models.permission import *


class Role(BaseModel):
    """
    Class that represents a role for users
    """

    __tablename__ = "role"

    name = db.Column(db.String(30), unique=True, nullable=False)
    permissions = db.Column(MutableList.as_mutable(PickleType), default=[])

    def __init__(self, name: str, permissions: List[str] = None):
        self.name = name
        self.permissions = permissions if permissions else []

    def add_permission(self, permission: str):
        # It must use a new list. It doesn't track changes if append + save is used.
        # We don't know why.
        self.permissions = self.permissions + [permission] if self.permissions else [permission]

    def _update(self, name: str = None, permissions: list = None, **kwargs):
        """
        Particular Role update method.
        """
        if name is not None:
            self.name = name
        if permissions is not None:
            self.permissions = permissions

    def __repr__(self):
        return f"<Role: name={self.name}, permissions={self.permissions}>"


class NullRole(NullBaseModel, Role):
    __abstract__ = True

    def __init__(self, id: int = None, name: str = None, permissions: List[str] = None):
        self.id = id
        self.name = name
        self.permissions = permissions if permissions else []