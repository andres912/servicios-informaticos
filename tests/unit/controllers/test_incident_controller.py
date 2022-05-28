from project.controllers.incident_controller import IncidentController
from project.models.incident import Incident
from project import db


def test_incident_creation(
    init_database, saved_user, saved_hardware_configuration_item
):

    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    INCIDENT_PRIORITY = "Alta"
    INCIDENT_CREATED_BY = saved_user.username
    INCIDENT_HARDWARE_CONFIGURATION_ITEMS = [saved_hardware_configuration_item]

    arguments = {
        "description": INCIDENT_DESCRIPTION,
        "priority": INCIDENT_PRIORITY,
        "created_by": INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }

    IncidentController.create(**arguments)

    incidents = IncidentController.load_all()
    assert len(incidents) == 1
    assert incidents[0].description == INCIDENT_DESCRIPTION
    assert incidents[0].priority == INCIDENT_PRIORITY
    assert incidents[0].created_by == INCIDENT_CREATED_BY
    assert incidents[0].hardware_configuration_items == [
        saved_hardware_configuration_item
    ]


def test_getting_incidentes_created_by_specific_user(
    init_database, saved_user, saved_alternative_user, saved_hardware_configuration_item
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "The computer is not working."
    FIRST_INCIDENT_CREATED_BY = saved_user.username
    SECOND_INCIDENT_CREATED_BY = saved_alternative_user.username
    INCIDENT_HARDWARE_CONFIGURATION_ITEMS = [saved_hardware_configuration_item]

    first_incident_arguments = {
        "description": FIRST_INCIDENT_DESCRIPTION,
        "created_by": FIRST_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }
    second_incident_arguments = {
        "description": SECOND_INCIDENT_DESCRIPTION,
        "created_by": SECOND_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }

    IncidentController.create(**first_incident_arguments)
    IncidentController.create(**second_incident_arguments)

    first_user_incidents = IncidentController.load_incidents_created_by_user(
        saved_user.username
    )
    second_user_incidents = IncidentController.load_incidents_created_by_user(
        saved_alternative_user.username
    )

    assert len(first_user_incidents) == 1
    assert len(second_user_incidents) == 1
    assert first_user_incidents[0].description == FIRST_INCIDENT_DESCRIPTION
    assert first_user_incidents[0].created_by == saved_user.username
    assert second_user_incidents[0].description == SECOND_INCIDENT_DESCRIPTION
    assert second_user_incidents[0].created_by == saved_alternative_user.username


def test_getting_incidentes_taken_by_specific_user(
    init_database, saved_user, saved_alternative_user, saved_hardware_configuration_item
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "The computer is not working."
    FIRST_INCIDENT_CREATED_BY = saved_user.username
    SECOND_INCIDENT_CREATED_BY = saved_alternative_user.username
    INCIDENT_HARDWARE_CONFIGURATION_ITEMS = [saved_hardware_configuration_item]

    first_incident_arguments = {
        "description": FIRST_INCIDENT_DESCRIPTION,
        "created_by": FIRST_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }
    second_incident_arguments = {
        "description": SECOND_INCIDENT_DESCRIPTION,
        "created_by": SECOND_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }

    first_incident = IncidentController.create(**first_incident_arguments)
    second_incident = IncidentController.create(**second_incident_arguments)

    IncidentController.assign_incident_to_user(first_incident.id, saved_user.username)
    IncidentController.assign_incident_to_user(
        second_incident.id, saved_alternative_user.username
    )

    first_user_incidents = IncidentController.load_incidents_assigned_to_user(
        saved_user.username
    )
    second_user_incidents = IncidentController.load_incidents_assigned_to_user(
        saved_alternative_user.username
    )

    assert len(first_user_incidents) == 1
    assert len(second_user_incidents) == 1
    assert first_user_incidents[0].taken_by == saved_user.username
    assert second_user_incidents[0].taken_by == saved_alternative_user.username


def test_getting_assigned_incidents_returns_all_incidents_that_have_been_assigned_to_someone(
    init_database, saved_user, saved_alternative_user, saved_hardware_configuration_item
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "The computer is not working."
    FIRST_INCIDENT_CREATED_BY = saved_user.username
    SECOND_INCIDENT_CREATED_BY = saved_alternative_user.username
    INCIDENT_HARDWARE_CONFIGURATION_ITEMS = [saved_hardware_configuration_item]

    first_incident_arguments = {
        "description": FIRST_INCIDENT_DESCRIPTION,
        "created_by": FIRST_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }
    second_incident_arguments = {
        "description": SECOND_INCIDENT_DESCRIPTION,
        "created_by": SECOND_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }
    unassigned_incident_arguments = {
        "description": "Unassigned incidents",
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }

    first_incident = IncidentController.create(**first_incident_arguments)
    second_incident = IncidentController.create(**second_incident_arguments)
    unassigned_incident = IncidentController.create(**unassigned_incident_arguments)

    IncidentController.assign_incident_to_user(first_incident.id, saved_user.username)
    IncidentController.assign_incident_to_user(
        second_incident.id, saved_alternative_user.username
    )

    assigned_incidents = IncidentController.load_assigned_incidents()

    assert len(assigned_incidents) == 2
    assert unassigned_incident not in assigned_incidents


def test_getting_unassigned_incidents_returns_all_incidents_that_have_not_yet_been_assigned_to_someone(
    init_database, saved_user, saved_alternative_user, saved_hardware_configuration_item
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "The computer is not working."
    FIRST_INCIDENT_CREATED_BY = saved_user.username
    SECOND_INCIDENT_CREATED_BY = saved_alternative_user.username
    INCIDENT_HARDWARE_CONFIGURATION_ITEMS = [saved_hardware_configuration_item]

    first_incident_arguments = {
        "description": FIRST_INCIDENT_DESCRIPTION,
        "created_by": FIRST_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }
    second_incident_arguments = {
        "description": SECOND_INCIDENT_DESCRIPTION,
        "created_by": SECOND_INCIDENT_CREATED_BY,
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }
    unassigned_incident_arguments = {
        "description": "Unassigned incidents",
        "hardware_configuration_items": INCIDENT_HARDWARE_CONFIGURATION_ITEMS,
    }

    first_incident = IncidentController.create(**first_incident_arguments)
    second_incident = IncidentController.create(**second_incident_arguments)
    unassigned_incident = IncidentController.create(**unassigned_incident_arguments)

    IncidentController.assign_incident_to_user(first_incident.id, saved_user.username)
    IncidentController.assign_incident_to_user(
        second_incident.id, saved_alternative_user.username
    )

    unassigned_incidents = IncidentController.load_unassigned_incidents()

    assert len(unassigned_incidents) == 1
    assert unassigned_incident in unassigned_incidents


def test_incident_deletion(init_database, saved_hardware_configuration_item):

    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    incident = IncidentController.create(
        description=INCIDENT_DESCRIPTION,
        hardware_configuration_items=[saved_hardware_configuration_item],
    )

    IncidentController.delete(incident.id)

    incidents = IncidentController.load_all()
    assert len(incidents) == 0


def test_deleting_all_incidents(init_database, saved_hardware_configuration_item):
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    INCIDENTS_AMOUNT = 10

    for i in range(INCIDENTS_AMOUNT):
        IncidentController.create(
        description=INCIDENT_DESCRIPTION,
        hardware_configuration_items=[saved_hardware_configuration_item],
    )

    starting_incidents_amount = len(IncidentController.load_all())

    IncidentController.delete_all()

    incidents = IncidentController.load_all()
    assert len(incidents) == starting_incidents_amount - INCIDENTS_AMOUNT


def test_retreiving_incident_configuration_items(
    init_database, saved_hardware_configuration_item, saved_incident
):

    configuration_item_incidents = saved_hardware_configuration_item.incidents
    incident_hardware_configuration_items = saved_incident.hardware_configuration_items

    assert len(configuration_item_incidents) == 1
    assert len(incident_hardware_configuration_items) == 1
    assert configuration_item_incidents[0].id == saved_incident.id
    assert incident_hardware_configuration_items[0].id == saved_hardware_configuration_item.id
