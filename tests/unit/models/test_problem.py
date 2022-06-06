from project.models.incident import Incident
from project.models.priority import *
from project.models.status import *
from project.models.user import User


def test_incident_creation(
    init_database, saved_user, saved_hardware_configuration_item
):

    PROBLEM_DESCRIPTION = "The server connection to the database is not working."
    PROBLEM_PRIORITY = PRIORITY_MEDIUM
    PROBLEM_CREATED_BY = saved_user.username

    incident = Incident(
        description=PROBLEM_DESCRIPTION,
        priority=PROBLEM_PRIORITY,
        created_by=PROBLEM_CREATED_BY,
        hardware_configuration_items=[saved_hardware_configuration_item],
    )

    assert incident.description == PROBLEM_DESCRIPTION
    assert incident.priority == PROBLEM_PRIORITY
    assert incident.status == STATUS_PENDING
    assert incident.created_by == PROBLEM_CREATED_BY
    assert incident.taken_by == None
    assert incident.hardware_configuration_items == [saved_hardware_configuration_item]


def create_random_user(db, saved_role):
    user = User(
        username="test_user",
        email="mail@fi.uba.ar",
        password="test_password",
        role=saved_role,
    )

    db.session.add(user)
    db.session.commit()
    return user


def test_change_incident_status(init_database, _db, saved_incident):
    NEW_STATUS = STATUS_IN_PROCESS
    saved_incident.change_status(NEW_STATUS)
    assert saved_incident.status == NEW_STATUS


def test_change_inicident_priority(init_database, _db, saved_incident):
    NEW_PRIORITY = PRIORITY_HIGH
    saved_incident.change_priority(NEW_PRIORITY)
    assert saved_incident.priority == NEW_PRIORITY


def test_take_incident(init_database, _db, saved_incident):
    saved_incident.assign_user(saved_incident.created_by)
    assert saved_incident.taken_by == saved_incident.created_by
