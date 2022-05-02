from project.models.user import User


def test_user_creation(init_database, saved_role):
    """
    Test user creation
    """
    USER_USERNAME = "test_user"
    USER_EMAIL = "mail@fi.uba.ar"
    USER_PASSWORD = "test_password"

    user = User(
        username=USER_USERNAME,
        email=USER_EMAIL,
        plaintext_password=USER_PASSWORD,
        role=saved_role,
    )

    assert user.username == USER_USERNAME
    assert user.email == USER_EMAIL
    assert user.is_correct_password(USER_PASSWORD)
    assert user.role.id == saved_role.id
