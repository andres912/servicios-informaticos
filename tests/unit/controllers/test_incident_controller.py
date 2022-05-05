from project.controllers.incident_controller import IncidentController
from project.models.incident import Incident
from project import db


def test_incident_saving(init_database):
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    incident = Incident(description=INCIDENT_DESCRIPTION)
    IncidentController.save(incident)

    incidents = IncidentController.load_all()
    assert len(incidents) == 1
    assert incidents[0].description == INCIDENT_DESCRIPTION


def test_getting_incidentes_created_by_specific_user(
    init_database, saved_user, saved_alternative_user
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "Heroku App is not working."
    first_incident = Incident(
        description=FIRST_INCIDENT_DESCRIPTION, created_by=saved_user.username
    )
    second_incident = Incident(
        description=SECOND_INCIDENT_DESCRIPTION,
        created_by=saved_alternative_user.username,
    )

    IncidentController.save(first_incident)
    IncidentController.save(second_incident)
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
    init_database, saved_user, saved_alternative_user
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "Heroku App is not working."
    first_incident = Incident(description=FIRST_INCIDENT_DESCRIPTION)
    second_incident = Incident(description=SECOND_INCIDENT_DESCRIPTION)
    IncidentController.save(first_incident)
    IncidentController.save(second_incident)

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
    assert first_user_incidents[0].description == FIRST_INCIDENT_DESCRIPTION
    assert first_user_incidents[0].taken_by == saved_user.username
    assert second_user_incidents[0].description == SECOND_INCIDENT_DESCRIPTION
    assert second_user_incidents[0].taken_by == saved_alternative_user.username


def test_getting_assigned_incidents_returns_all_incidents_that_have_been_assigned_to_someone(
    init_database, saved_user, saved_alternative_user
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "Heroku App is not working."
    first_incident = Incident(description=FIRST_INCIDENT_DESCRIPTION)
    second_incident = Incident(description=SECOND_INCIDENT_DESCRIPTION)
    unassigned_incident = Incident(description="Unassigned incident")
    IncidentController.save(first_incident)
    IncidentController.save(second_incident)
    IncidentController.save(unassigned_incident)

    IncidentController.assign_incident_to_user(first_incident.id, saved_user.username)
    IncidentController.assign_incident_to_user(
        second_incident.id, saved_alternative_user.username
    )

    assigned_incidents = IncidentController.load_assigned_incidents()

    assert len(assigned_incidents) == 2
    assert unassigned_incident not in assigned_incidents


def test_getting_unassigned_incidents_returns_all_incidents_that_have_not_yet_been_assigned_to_someone(
    init_database, saved_user, saved_alternative_user
):
    FIRST_INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    SECOND_INCIDENT_DESCRIPTION = "Heroku App is not working."
    first_incident = Incident(description=FIRST_INCIDENT_DESCRIPTION)
    second_incident = Incident(description=SECOND_INCIDENT_DESCRIPTION)
    unassigned_incident = Incident(description="Unassigned incident")
    IncidentController.save(first_incident)
    IncidentController.save(second_incident)
    IncidentController.save(unassigned_incident)

    IncidentController.assign_incident_to_user(first_incident.id, saved_user.username)
    IncidentController.assign_incident_to_user(
        second_incident.id, saved_alternative_user.username
    )

    unassigned_incidents = IncidentController.load_unassigned_incidents()

    assert len(unassigned_incidents) == 1
    assert unassigned_incident in unassigned_incidents


def test_incident_deleting(init_database):
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    incident = Incident(description=INCIDENT_DESCRIPTION)

    IncidentController.save(incident)
    IncidentController.delete(incident.id)

    incidents = IncidentController.load_all()
    assert len(incidents) == 0


def test_deleting_all_incidents(init_database):
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    INCIDENTS_AMOUNT = 10
    for i in range(INCIDENTS_AMOUNT):
        incident = Incident(description=INCIDENT_DESCRIPTION)
        IncidentController.save(incident)

    IncidentController.delete_all()

    incidents = IncidentController.load_all()
    assert len(incidents) == 0
