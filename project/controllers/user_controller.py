from typing import Any, List

from project import db
from project.controllers.enableable_object_controller import EnableableObjectController
from project.controllers.role_controller import RoleController
from project.models.exceptions import ValidationError
from project.models.user import User
from project.controllers.base_controller import InexistentBaseModelInstance


def get_validation_error_message(
    obj_name: str, parameter: str, comment: str, comment_es: str, value: Any = None
):
    return {
        "error": f"invalid_{obj_name}",
        "parameter": parameter,
        "value": value,
        "description": f"The given {parameter} {comment}",
        "description_es": f"{comment_es}",
    }


class UserController(EnableableObjectController):
    object_class = User
    null_object_class = None

    @staticmethod
    def _verify_relations(new_user: User) -> None:
        """
        No verifications needed.
        """
        pass

    @classmethod
    def load_updated(cls, id: int, **kwargs) -> User:
        """
        Receives a user id and additional arguments.
        Loads pharmacy, distributor or pharma group if they need to be loaded to update the user.
        """
        return super().load_updated(id, **kwargs)

    @classmethod
    def _update(cls, user: User, role_id: int = None, **kwargs) -> None:
        """
        Receives a user, a role id and additional arguments.
        Updates the user with new data.
        """
        role = RoleController.load_by_id(role_id) if role_id else user.role
        updated_user = user.update(role=role, **kwargs)

    @classmethod
    def load(cls, username: str, password: str) -> User:
        """
        Used by login.
        Receives a username & password and verifies if they are correct.
        Returns the user if data is correct.
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise InexistentBaseModelInstance("user", "username", username)
        if not user.is_correct_password(password):
            raise ValidationError(
                message=[
                    get_validation_error_message(
                        "user", "password", "is invalid", "La contraseña es invalida"
                    )
                ]
            )
        return user

    @classmethod
    def load_enabled(cls, id: int) -> None:
        """
        Receives an id of a Model object.
        Loads and updates (enables) the object through the base controller method.
        Returns the updated object.
        """
        return cls.load_updated(id=id, is_enabled=True)

    @classmethod
    def load_by_email(cls, username: str, email: str):
        """
        Receives a username and email and queries for its User.
        Returns only one User or raises an error if it's not found.
        """
        user = User.query.filter_by(email=email, username=username).first()
        if not user:
            raise InexistentBaseModelInstance("user", "email", email)
        return user

    @classmethod
    def load_by_username(cls, username: str):
        """
        Receives a username and email and queries for its User.
        Returns only one User or raises an error if it's not found.
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise InexistentBaseModelInstance("user", username)
        return user

    @classmethod
    def verify_existent_active_user(cls, username: str) -> bool:
        """
        Receives a username and verifies existence, if it exists it raises an error.
        Otherwise returns True by default.
        """
        user_by_username = User.query.filter_by(
            username=username, is_deleted=False
        ).first()
        if user_by_username:
            raise ValidationError(
                message=[
                    get_validation_error_message(
                        "user",
                        "username",
                        "already exists",
                        "El usuario ya existe",
                        value=username,
                    )
                ]
            )
        return True

    # NOT USED BUT FUNCTIONAL
    @classmethod
    def load_visibles(cls) -> List[User]:
        """
        Returns a list of users that are visible.
        """
        return cls.object_class.query.filter_by(is_visible=True).all()

    @classmethod
    def set_as_logged(cls, user: User) -> None:
        """
        Receives a user and updates its last login time.
        """
        user.touch()
        db.session.commit()

    @classmethod
    def create(
        cls,
        username,
        email,
        password,
        role_id,
        is_visible: bool = True,
        name: str = None,
        lastname: str = None,
    ) -> User:
        """
        Receives user data and additional arguments.
        Calls UserCreator to create the user.
        Returns a new user.
        """

        is_user_deleted = cls.is_user_deleted(username)
        if is_user_deleted:
            user = User.query.filter_by(username=username).first()
            user.update(is_deleted=False)
            return user

        # Verify existent user, if there is an error it will be raised
        cls.verify_existent_active_user(username)

        role = RoleController.load_by_id(role_id)

        new_user = User(
            username=username,
            email=email,
            plaintext_password=password,
            role=role,
            is_visible=is_visible,
            name=name,
            lastname=lastname,
        )

        return new_user

    @classmethod
    def is_user_deleted(cls, username: str) -> bool:
        """
        Receives a username and verifies if the user is deleted.
        Returns True if the user is deleted.
        """
        user = User.query.filter_by(username=username).first()
        return user.is_deleted if user else False
