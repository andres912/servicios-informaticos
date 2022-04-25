def test_incident_post(test_client, init_database):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """
    INCIDENT_TITLE = "Incident with server connection to the database"
    INCIDENT_DESCRIPTION = "The server connection to the database is not working."

    response = test_client.post(
        "/incidents",
        json={
            "title": INCIDENT_TITLE,
            "description": INCIDENT_DESCRIPTION
        }
    )
    assert response.status_code == 200
    assert response.json["title"] == INCIDENT_TITLE
    assert response.json["description"] == INCIDENT_DESCRIPTION