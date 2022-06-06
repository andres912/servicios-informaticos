from project.models.priority import *
from project.models.status import *


def test_incident_post(test_client, init_database, saved_user, saved_incident):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """
    PROBLEM_DESCRIPTION = "The server connection to the database is not working."
    PROBLEM_PRIORITY = PRIORITY_MEDIUM
    PROBLEM_CREATED_BY = saved_user.username
    PROBLEM_IMPACT = IMPACT_LOW
    PROBLEM_CAUSE = "Database too slow"


    response = test_client.post(
        "/problems",
        json={
            "description": PROBLEM_DESCRIPTION,
            "priority": PROBLEM_PRIORITY,
            "created_by": PROBLEM_CREATED_BY,
            "incident_name_0": saved_incident.description,
            "impact": PROBLEM_IMPACT,
            "cause": PROBLEM_CAUSE
        }
    )
    assert response.status_code == 200
    assert response.json["description"] == PROBLEM_DESCRIPTION
    assert response.json["priority"] == PROBLEM_PRIORITY
    assert response.json["status"] == STATUS_PENDING
    assert response.json["created_by"] == PROBLEM_CREATED_BY
    assert response.json["impact"] == PROBLEM_IMPACT
    assert response.json["cause"] == PROBLEM_CAUSE
    assert len(response.json["incidents"]) == 1
    assert response.json["incidents"][0]["description"] == saved_incident.description
