from project.models.priority import *
from project.models.status import *


def test_incident_post(test_client, init_database, saved_user, saved_hardware_configuration_item):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."
    INCIDENT_PRIORITY = PRIORITY_MEDIUM
    INCIDENT_CREATED_BY = saved_user.username
    hardware_configuration_items = [saved_hardware_configuration_item.id]

    response = test_client.post(
        "/incidents",
        json={
            "description": INCIDENT_DESCRIPTION,
            "priority": INCIDENT_PRIORITY,
            "created_by": INCIDENT_CREATED_BY,
            "hardware_configuration_items": hardware_configuration_items,
        }
    )
    assert response.status_code == 200
    assert response.json["description"] == INCIDENT_DESCRIPTION
    assert response.json["priority"] == INCIDENT_PRIORITY
    assert response.json["status"] == STATUS_PENDING
    assert response.json["created_by"] == INCIDENT_CREATED_BY