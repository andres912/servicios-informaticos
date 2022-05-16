from datetime import datetime
import os
from project import create_app, db
import pytest
from project.models.configuration_item.hardware_configuration_item import HardwareConfigurationItem
from project.models.configuration_item.software_configuration_item import SoftwareConfigurationItem
from project.models.configuration_item.sla_configuration_item import SLAConfigurationItem
from project.models.incident import Incident
from project.models.priority import PRIORITY_MEDIUM

from project.models.role import Role
from project.models.user import User

@pytest.fixture(scope="function")
def test_client():
    os.environ["TESTING"] = "True"
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
def saved_incident(saved_user, saved_hardware_configuration_item):
    incident = Incident(
        description="Generic description",
        priority=PRIORITY_MEDIUM,
        created_by=saved_user.username,
        hardware_configuration_items=[saved_hardware_configuration_item],
    )

    db.session.add(incident)
    db.session.commit()
    return incident

@pytest.fixture(scope="function")
def saved_hardware_configuration_item():
    item = HardwareConfigurationItem(
        name="Generic CI",
        description="Generic description",
        type="Generic type",
        manufacturer="Generic manufacturer",
        serial_number="XXXX-XXXX",
        price=100,
        purchase_date=datetime.now(),
    )

    db.session.add(item)
    db.session.commit()
    return item

@pytest.fixture(scope="function")
def saved_sla_configuration_item():
    item = SLAConfigurationItem(
        name="Generic CI",
        description="Generic description",
        service_type = "Generic type",
        service_manager = "Generic manager",
        client = "Generic client",
        starting_date = datetime.now(),
        ending_date = datetime.now(),
        measurement_unit = "Generic unit",
        measurement_value = 100,
    )

    db.session.add(item)
    db.session.commit()
    return item

@pytest.fixture(scope="function")
def saved_software_configuration_item():
    item = SoftwareConfigurationItem(
        name="Generic CI",
        description="Generic description",
        type = "Generic type",
        provider = "Generic provider",
        software_version = "10.0.0"
    )

    db.session.add(item)
    db.session.commit()
    return item