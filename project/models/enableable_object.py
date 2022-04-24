from project import db
from project.models.base_model import BaseModel, NullBaseModel

class EnableableObject(BaseModel):
    """
    Interface for object with capability to be enabled and disabled.
    """

    __abstract__ = True
    is_enabled = db.Column(db.Boolean, default=True)

    def _update(self, is_enabled=None, **kwargs):
        """
        Particular Enableable object update method.
        """
        if is_enabled is not None:
            self.is_enabled = is_enabled


class NullEnableableObject(NullBaseModel):
    __abstract__ = True
    is_enabled = False

    def _update(self, is_enabled=None):
        pass
