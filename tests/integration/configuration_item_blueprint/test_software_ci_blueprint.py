from numpy import save
from project.controllers.configuration_item_controller.software_ci_controller import SoftwareConfigurationItemController
from project.models.priority import *
from project.models.status import *
from datetime import datetime


def test_software_ci_creation(test_client, init_database, saved_user):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """

    ITEM_NAME = "Server"
    ITEM_DESCRIPTION = "Server"
    ITEM_TYPE = "Type"
    ITEM_PROVIDER = "Provider"
    ITEM_SOFTWARE_VERSION = "1.0"

    payload = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "type": ITEM_TYPE,
        "provider": ITEM_PROVIDER,
        "software_version": ITEM_SOFTWARE_VERSION,
    }

    response = test_client.post("/configuration-items/software", json=payload)

    assert response.status_code == 200
    assert response.json["id"]
    assert response.json["name"] == ITEM_NAME
    assert response.json["description"] == ITEM_DESCRIPTION
    assert response.json["type"] == ITEM_TYPE
    assert response.json["provider"] == ITEM_PROVIDER
    assert response.json["software_version"] == ITEM_SOFTWARE_VERSION

def test_software_ci_update(
    test_client, init_database, saved_user, saved_software_configuration_item
):
    """
    GIVEN I am an authenticated user
    WHEN I want to create an incident
    THEN the incident is created correctly
    """

    NEW_ITEM_NAME = "New Server"
    NEW_ITEM_DESCRIPTION = "New Server"
    NEW_ITEM_TYPE = "New Type"
    NEW_ITEM_PROVIDER = "New Provider"
    NEW_ITEM_SOFTWARE_VERSION = "2.0"
    
    payload = {
        "name": NEW_ITEM_NAME,
        "description": NEW_ITEM_DESCRIPTION,
        "type": NEW_ITEM_TYPE,
        "provider": NEW_ITEM_PROVIDER,
        "software_version": NEW_ITEM_SOFTWARE_VERSION,
    }

    response = test_client.put(
        f"/configuration-items/software/{saved_software_configuration_item.id}",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json["id"] == saved_software_configuration_item.id
    assert response.json["name"] == NEW_ITEM_NAME
    assert response.json["description"] == NEW_ITEM_DESCRIPTION
    assert response.json["type"] == NEW_ITEM_TYPE
    assert response.json["provider"] == NEW_ITEM_PROVIDER
    assert response.json["software_version"] == NEW_ITEM_SOFTWARE_VERSION

def test_software_ci_delete(
    test_client, init_database, saved_user, saved_software_configuration_item
):
    """
    Tests the deletion of a software configuration item
    """

    item_initial_quantity = len(SoftwareConfigurationItemController.load_all())

    response = test_client.delete(
        f"/configuration-items/software/{saved_software_configuration_item.id}"
    )

    item_final_quantity = len(SoftwareConfigurationItemController.load_all())

    assert response.status_code == 200
    assert response.json["id"] == saved_software_configuration_item.id
    assert item_initial_quantity - 1 == item_final_quantity

def test_software_ci_get_all(
    test_client, init_database, saved_user, saved_software_configuration_item
):
    """
    Tests the retrieval of all software configuration items
    """

    response = test_client.get(
        f"/configuration-items/software"
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == saved_software_configuration_item.current_version.id
    assert response.json[0]["name"] == saved_software_configuration_item.current_version.name
    assert response.json[0]["description"] == saved_software_configuration_item.current_version.description
    assert response.json[0]["type"] == saved_software_configuration_item.current_version.type
    assert response.json[0]["provider"] == saved_software_configuration_item.current_version.provider
    assert response.json[0]["software_version"] == saved_software_configuration_item.current_version.software_version