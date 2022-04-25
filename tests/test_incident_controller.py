from project.controllers.incident_controller import IncidentController
from project.models.incident import Incident
from project import db

def test_incident_saving(init_database):
    INCIDENT_TITLE = "Incident with server connection to the database"
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    incident = Incident(title=INCIDENT_TITLE, description=INCIDENT_DESCRIPTION)
    IncidentController.save(incident)
    
    incidents = IncidentController.load_all()
    assert len(incidents) == 1
    assert incidents[0].title == INCIDENT_TITLE
    assert incidents[0].description == INCIDENT_DESCRIPTION