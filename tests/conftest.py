from project import create_app, db
import pytest
from project.models.incident import Incident
from project.models.priority import PRIORITY_MEDIUM

from project.models.role import Role
from project.models.user import User

@pytest.fixture(scope="function")
def test_client():
    flask_app = create_app("flask_test.cfg")
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope="function")
def init_database(test_client):
    db.create_all()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()

@pytest.fixture(scope="function")
def _db():
    return db


@pytest.fixture(scope="function")
def saved_role():
    role = Role(name="admin", permissions=["total_access"])
    db.session.add(role)
    db.session.commit()
    return role


@pytest.fixture(scope="function")
def saved_user(saved_role):
    user = User(
        username="test_user",
        email="mail@fi.uba.ar",
        plaintext_password="test_password",
        role=saved_role,
    )

    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope="function")
def saved_alternative_user(saved_role):
    user = User(
        username="alternative_user",
        email="alternative_mail@fi.uba.ar",
        plaintext_password="alternative_password",
        role=saved_role,
    )

    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope="function")
def saved_incident(saved_user):
    incident = Incident(
        description="Generic description",
        priority=PRIORITY_MEDIUM,
        created_by=saved_user.username,
    )

    db.session.add(incident)
    db.session.commit()
    return incident