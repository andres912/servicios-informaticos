from project.controllers.base_controller import BaseController
from project.models.enableable_object import EnableableObject


class EnableableObjectController(BaseController):
    """
    Base controller for the Enableable objects.
    Implements generic enable and disable to all Model classes.
    """

    object_class = EnableableObject
    null_object_class = None

    @classmethod
    def load_enabled(cls, id: int) -> None:
        """
        Receives an id of a Model object.
        Loads and updates (enables) the object through the base controller method.
        Returns the updated object.
        """
        return cls.load_updated(id=id, is_enabled=True)

    @classmethod
    def load_disabled(cls, id: int) -> None:
        """
        Receives an id of a Model object.
        Loads and updates (disables) the object through the base controller method.
        Returns the updated object.
        """
        return cls.load_updated(id=id, is_enabled=False)