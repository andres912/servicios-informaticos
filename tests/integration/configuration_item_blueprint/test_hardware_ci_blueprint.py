from numpy import save
from project.controllers.configuration_item_controller.hardware_ci_controller import HardwareConfigurationItemController
from project.models.priority import *
from project.models.status import *
from datetime import datetime


def test_hardware_ci_creation(test_client, init_database, saved_user):
    """
    Tests de creation of a hardware configuration item
    """

    ITEM_NAME = "Server"
    ITEM_DESCRIPTION = "Server"
    ITEM_TYPE = "Server"
    ITEM_PURCHASE_DATE = "21/04/2022"
    ITEM_MANUFACTURER = "Dell"
    ITEM_SERIAL_NUMBER = "123456789"
    ITEM_PRICE = 10

    payload = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "type": ITEM_TYPE,
        "purchase_date": ITEM_PURCHASE_DATE,
        "manufacturer": ITEM_MANUFACTURER,
        "serial_number": ITEM_SERIAL_NUMBER,
        "price": ITEM_PRICE,
    }

    response = test_client.post("/configuration-items/hardware", json=payload)

    assert response.status_code == 200
    assert response.json["id"]
    assert response.json["name"] == ITEM_NAME
    assert response.json["description"] == ITEM_DESCRIPTION
    assert response.json["type"] == ITEM_TYPE
    assert response.json["purchase_date"] == ITEM_PURCHASE_DATE
    assert response.json["manufacturer"] == ITEM_MANUFACTURER
    assert response.json["serial_number"] == ITEM_SERIAL_NUMBER
    assert response.json["price"] == ITEM_PRICE


def test_hardware_ci_update(
    test_client, init_database, saved_user, saved_hardware_configuration_item
):
    """
    Tests the update of a hardware configuration item
    """

    NEW_ITEM_NAME = "Server"
    NEW_ITEM_DESCRIPTION = "Server"
    NEW_ITEM_TYPE = "Server"
    NEW_ITEM_PURCHASE_DATE = "21/04/2022"
    NEW_ITEM_MANUFACTURER = "Dell"
    NEW_ITEM_SERIAL_NUMBER = "123456789"
    NEW_ITEM_PRICE = 10

    payload = {
        "name": NEW_ITEM_NAME,
        "description": NEW_ITEM_DESCRIPTION,
        "type": NEW_ITEM_TYPE,
        "purchase_date": NEW_ITEM_PURCHASE_DATE,
        "manufacturer": NEW_ITEM_MANUFACTURER,
        "serial_number": NEW_ITEM_SERIAL_NUMBER,
        "price": NEW_ITEM_PRICE,
    }

    response = test_client.put(
        f"/configuration-items/hardware/{saved_hardware_configuration_item.id}",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json["id"] == saved_hardware_configuration_item.id
    assert response.json["name"] == NEW_ITEM_NAME
    assert response.json["description"] == NEW_ITEM_DESCRIPTION
    assert response.json["type"] == NEW_ITEM_TYPE
    assert response.json["purchase_date"] == NEW_ITEM_PURCHASE_DATE
    assert response.json["manufacturer"] == NEW_ITEM_MANUFACTURER
    assert response.json["serial_number"] == NEW_ITEM_SERIAL_NUMBER
    assert response.json["price"] == NEW_ITEM_PRICE

def test_hardware_ci_delete(
    test_client, init_database, saved_user, saved_hardware_configuration_item
):
    """
    Tests the deletion of a hardware configuration item
    """

    item_initial_quantity = len(HardwareConfigurationItemController.load_all())

    response = test_client.delete(
        f"/configuration-items/hardware/{saved_hardware_configuration_item.id}"
    )

    item_final_quantity = len(HardwareConfigurationItemController.load_all())

    assert response.status_code == 200
    assert response.json["id"] == saved_hardware_configuration_item.id
    assert item_initial_quantity - 1 == item_final_quantity

def test_hardware_ci_get_all(
    test_client, init_database, saved_user, saved_hardware_configuration_item
):
    """
    Tests the retrieval of all hardware configuration items
    """

    response = test_client.get(
        f"/configuration-items/hardware"
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == saved_hardware_configuration_item.id
    assert response.json[0]["name"] == saved_hardware_configuration_item.name
    assert response.json[0]["description"] == saved_hardware_configuration_item.description
    assert response.json[0]["type"] == saved_hardware_configuration_item.type
    assert response.json[0]["manufacturer"] == saved_hardware_configuration_item.manufacturer
    assert response.json[0]["serial_number"] == saved_hardware_configuration_item.serial_number
    assert response.json[0]["price"] == saved_hardware_configuration_item.price