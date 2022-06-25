from numpy import save
from project.controllers.configuration_item_controller.sla_ci_controller import SLAConfigurationItemController
from project.models.priority import *
from project.models.status import *
from datetime import datetime


def test_sla_ci_creation(test_client, init_database, saved_user):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """

    ITEM_NAME = "Server"
    ITEM_DESCRIPTION = "Server"
    SERVICE_TYPE = "Service Type"
    SERVICE_MANAGER = "Service Manager"
    CLIENT = "Client"
    STARTING_DATE = "21/04/2022"
    ENDING_DATE = "21/04/2023"
    MEASUREMENT_UNIT = "Days"
    MEASUREMENT_VALUE = 10

    payload = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "service_type": SERVICE_TYPE,
        "service_manager": SERVICE_MANAGER,
        "client": CLIENT,
        "starting_date": STARTING_DATE,
        "ending_date": ENDING_DATE,
        "measurement_unit": MEASUREMENT_UNIT,
        "measurement_value": MEASUREMENT_VALUE,
    }

    response = test_client.post("/configuration-items/sla", json=payload)

    assert response.status_code == 200
    assert response.json["id"]
    assert response.json["name"] == ITEM_NAME
    assert response.json["description"] == ITEM_DESCRIPTION
    assert response.json["service_type"] == SERVICE_TYPE
    assert response.json["service_manager"] == SERVICE_MANAGER
    assert response.json["client"] == CLIENT
    assert response.json["starting_date"] == STARTING_DATE
    assert response.json["ending_date"] == ENDING_DATE
    assert response.json["measurement_unit"] == MEASUREMENT_UNIT
    assert response.json["measurement_value"] == MEASUREMENT_VALUE

def test_sla_ci_update(
    test_client, init_database, saved_user, saved_sla_configuration_item
):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """

    NEW_ITEM_NAME = "New Server"
    NEW_ITEM_DESCRIPTION = "New Server"
    NEW_ITEM_SERVICE_TYPE = "New Service Type"
    NEW_ITEM_SERVICE_MANAGER = "New Service Manager"
    NEW_ITEM_CLIENT = "New Client"
    NEW_ITEM_STARTING_DATE = "22/04/2022"
    NEW_ITEM_ENDING_DATE = "22/04/2023"
    NEW_ITEM_MEASUREMENT_UNIT = "Months"
    NEW_ITEM_MEASUREMENT_VALUE = 20

    payload = {
        "name": NEW_ITEM_NAME,
        "description": NEW_ITEM_DESCRIPTION,
        "service_type": NEW_ITEM_SERVICE_TYPE,
        "service_manager": NEW_ITEM_SERVICE_MANAGER,
        "client": NEW_ITEM_CLIENT,
        "starting_date": NEW_ITEM_STARTING_DATE,
        "ending_date": NEW_ITEM_ENDING_DATE,
        "measurement_unit": NEW_ITEM_MEASUREMENT_UNIT,
        "measurement_value": NEW_ITEM_MEASUREMENT_VALUE,
    }

    response = test_client.put(
        f"/configuration-items/sla/{saved_sla_configuration_item.id}",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json["id"] == saved_sla_configuration_item.id
    assert response.json["name"] == NEW_ITEM_NAME
    assert response.json["description"] == NEW_ITEM_DESCRIPTION
    assert response.json["service_type"] == NEW_ITEM_SERVICE_TYPE
    assert response.json["service_manager"] == NEW_ITEM_SERVICE_MANAGER
    assert response.json["client"] == NEW_ITEM_CLIENT
    assert response.json["starting_date"] == NEW_ITEM_STARTING_DATE
    assert response.json["ending_date"] == NEW_ITEM_ENDING_DATE
    assert response.json["measurement_unit"] == NEW_ITEM_MEASUREMENT_UNIT
    assert response.json["measurement_value"] == NEW_ITEM_MEASUREMENT_VALUE

def test_sla_ci_delete(
    test_client, init_database, saved_user, saved_sla_configuration_item
):
    """
    Tests the deletion of a sla configuration item
    """

    item_initial_quantity = len(SLAConfigurationItemController.load_all())

    response = test_client.delete(
        f"/configuration-items/sla/{saved_sla_configuration_item.id}"
    )

    item_final_quantity = len(SLAConfigurationItemController.load_all())

    assert response.status_code == 200
    assert response.json["id"] == saved_sla_configuration_item.id
    assert item_initial_quantity - 1 == item_final_quantity

def test_sla_ci_get_all(
    test_client, init_database, saved_user, saved_sla_configuration_item
):
    """
    Tests the retrieval of all sla configuration items
    """

    response = test_client.get(
        f"/configuration-items/sla"
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == saved_sla_configuration_item.current_version.id
    assert response.json[0]["name"] == saved_sla_configuration_item.current_version.name
    assert response.json[0]["description"] == saved_sla_configuration_item.current_version.description
    assert response.json[0]["service_type"] == saved_sla_configuration_item.current_version.service_type
    assert response.json[0]["service_manager"] == saved_sla_configuration_item.current_version.service_manager
    assert response.json[0]["client"] == saved_sla_configuration_item.current_version.client
    assert response.json[0]["measurement_unit"] == saved_sla_configuration_item.current_version.measurement_unit
    assert response.json[0]["measurement_value"] == saved_sla_configuration_item.current_version.measurement_value