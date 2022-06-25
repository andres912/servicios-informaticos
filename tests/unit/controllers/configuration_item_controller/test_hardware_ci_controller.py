from datetime import datetime
from project.controllers.configuration_item_controller.hardware_ci_controller import HardwareConfigurationItemController
from project.models.incident import Incident
from project import db


def test_hardware_ci_item_creation(init_database):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_TYPE = "Test Type"
    ITEM_MANUFACTURER = "Test Manufacturer"
    ITEM_SERIAL_NUMBER = "Test Serial Number"
    ITEM_PRICE = 10
    ITEM_PURCHASE_DATE = datetime.now()

    kwargs = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "type": ITEM_TYPE,
        "manufacturer": ITEM_MANUFACTURER,
        "serial_number": ITEM_SERIAL_NUMBER,
        "price": ITEM_PRICE,
        "purchase_date": ITEM_PURCHASE_DATE,
    }


    item = HardwareConfigurationItemController.create(**kwargs)

    assert item.current_version.name == ITEM_NAME
    assert item.current_version.description == ITEM_DESCRIPTION
    assert item.current_version.type == ITEM_TYPE
    assert item.current_version.manufacturer == ITEM_MANUFACTURER
    assert item.current_version.serial_number == ITEM_SERIAL_NUMBER
    assert item.current_version.price == ITEM_PRICE
    assert item.current_version.purchase_date == ITEM_PURCHASE_DATE

def test_hardware_ci_item_update(init_database):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_TYPE = "Test Type"
    ITEM_MANUFACTURER = "Test Manufacturer"
    ITEM_SERIAL_NUMBER = "Test Serial Number"
    ITEM_PRICE = 10
    ITEM_PURCHASE_DATE = datetime.now()

    kwargs = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "type": ITEM_TYPE,
        "manufacturer": ITEM_MANUFACTURER,
        "serial_number": ITEM_SERIAL_NUMBER,
        "price": ITEM_PRICE,
        "purchase_date": ITEM_PURCHASE_DATE,
    }

    item = HardwareConfigurationItemController.create(**kwargs)

    new_datetime = datetime.now()

    ITEM_NEW_NAME = "New Test Item"
    ITEM_NEW_DESCRIPTION = "New Test Description"
    ITEM_NEW_TYPE = "New Test Type"
    ITEM_NEW_MANUFACTURER = "New Test Manufacturer"
    ITEM_NEW_SERIAL_NUMBER = "New Test Serial Number"
    ITEM_NEW_PRICE = 20
    ITEM_NEW_PURCHASE_DATE = new_datetime

    kwargs = {
        "name": ITEM_NEW_NAME,
        "description": ITEM_NEW_DESCRIPTION,
        "type": ITEM_NEW_TYPE,
        "manufacturer": ITEM_NEW_MANUFACTURER,
        "serial_number": ITEM_NEW_SERIAL_NUMBER,
        "price": ITEM_NEW_PRICE,
        "purchase_date": ITEM_NEW_PURCHASE_DATE,
    }

    item = HardwareConfigurationItemController.update(item.id, **kwargs)

    assert item.current_version.name == ITEM_NEW_NAME
    assert item.current_version.description == ITEM_NEW_DESCRIPTION
    assert item.current_version.type == ITEM_NEW_TYPE
    assert item.current_version.manufacturer == ITEM_NEW_MANUFACTURER
    assert item.current_version.serial_number == ITEM_NEW_SERIAL_NUMBER
    assert item.current_version.price == ITEM_NEW_PRICE
    assert item.current_version.purchase_date == ITEM_NEW_PURCHASE_DATE





    
