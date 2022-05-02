import pytest
from datetime import datetime
from project.controllers.user_controller import UserController
from project.controllers.base_controller import (
    InexistentBaseModelInstance,
    ValidationError,
)
from project.models.user import User, UserEntity
from project.models.role import Role


def test_user_creation(init_database, _db, saved_role):
    """
    Test user creation throug user controller
    """
    USER_USERNAME = "test_user"
    USER_EMAIL = "mail@fi.uba.ar"
    USER_PASSWORD = "test_password"
    ROLE_ID = saved_role.id
    USER_NAME = "name"
    USER_LAST_NAME = "last_name"

    user = UserController.create(
        username=USER_USERNAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
        role_id=ROLE_ID,
        name=USER_NAME,
        lastname=USER_LAST_NAME,
    )

    users_saved = UserController.load_all()

    assert len(users_saved) == 1
    assert user.username == USER_USERNAME
    assert user.email == USER_EMAIL
    assert user.is_correct_password(USER_PASSWORD)
    assert user.role.id == ROLE_ID
    assert user.name == USER_NAME
    assert user.lastname == USER_LAST_NAME


def test_user_deletion(init_database, _db, saved_user):
    """
    Test user deletion through user controller
    """

    UserController.delete(saved_user.id)
    users_saved = UserController.load_all()

    assert len(users_saved) == 0


def test_user_modification(init_database, _db, saved_role):
    """
    Test user deletion through user controller
    """

    USER_USERNAME = "test_user"
    USER_EMAIL = "mail@fi.uba.ar"
    USER_PASSWORD = "test_password"
    ROLE_ID = saved_role.id
    USER_NAME = "name"
    USER_LAST_NAME = "last_name"

    user = UserController.create(
        username=USER_USERNAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
        role_id=ROLE_ID,
        name=USER_NAME,
        lastname=USER_LAST_NAME,
    )

    NEW_USER_NAME = "new_name"
    UserController._update(user, username=NEW_USER_NAME)
    updated_user = UserController.load_by_username(NEW_USER_NAME)
    assert updated_user.username == NEW_USER_NAME
