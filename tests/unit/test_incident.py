from project.models.incident import Incident

def test_incident_creation():
    INCIDENT_TITLE = "Incident with server connection to the database"
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    incident  = Incident(title=INCIDENT_TITLE, description=INCIDENT_DESCRIPTION)
    assert incident.title == INCIDENT_TITLE
    assert incident.description == INCIDENT_DESCRIPTION