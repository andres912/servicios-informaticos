from datetime import datetime
from project.controllers.configuration_item_controller.sla_ci_controller import SLAConfigurationItemController
from project import db


def test_hardware_ci_item_creation(init_database):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_SERVICE_TYPE = "Test Service Type"
    ITEM_SERVICE_MANAGER = "Test Service Manager"
    ITEM_CLIENT = "Test Client"
    ITEM_STARTING_DATE = datetime.now()
    ITEM_ENDING_DATE = datetime.now()
    ITEM_MEASUREMENT_UNIT = "Test Measurement Unit"
    ITEM_MEASUREMENT_VALUE = 10
    IS_CRUCIAL = True


    kwargs = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "version": ITEM_VERSION,
        "service_type": ITEM_SERVICE_TYPE,
        "service_manager": ITEM_SERVICE_MANAGER,
        "client": ITEM_CLIENT,
        "starting_date": ITEM_STARTING_DATE,
        "ending_date": ITEM_ENDING_DATE,
        "measurement_unit": ITEM_MEASUREMENT_UNIT,
        "measurement_value": ITEM_MEASUREMENT_VALUE,
        "is_crucial": IS_CRUCIAL
    }


    item = SLAConfigurationItemController.create(**kwargs)

    assert item.name == ITEM_NAME
    assert item.description == ITEM_DESCRIPTION
    assert item.version == ITEM_VERSION
    assert item.service_type == ITEM_SERVICE_TYPE
    assert item.service_manager == ITEM_SERVICE_MANAGER
    assert item.client == ITEM_CLIENT
    assert item.starting_date == ITEM_STARTING_DATE
    assert item.ending_date == ITEM_ENDING_DATE
    assert item.measurement_unit == ITEM_MEASUREMENT_UNIT
    assert item.measurement_value == ITEM_MEASUREMENT_VALUE
    assert item.is_crucial == IS_CRUCIAL

def test_hardware_ci_item_update(init_database):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_SERVICE_TYPE = "Test Service Type"
    ITEM_SERVICE_MANAGER = "Test Service Manager"
    ITEM_CLIENT = "Test Client"
    ITEM_STARTING_DATE = datetime.now()
    ITEM_ENDING_DATE = datetime.now()
    ITEM_MEASUREMENT_UNIT = "Test Measurement Unit"
    ITEM_MEASUREMENT_VALUE = 10
    IS_CRUCIAL = True


    kwargs = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "version": ITEM_VERSION,
        "service_type": ITEM_SERVICE_TYPE,
        "service_manager": ITEM_SERVICE_MANAGER,
        "client": ITEM_CLIENT,
        "starting_date": ITEM_STARTING_DATE,
        "ending_date": ITEM_ENDING_DATE,
        "measurement_unit": ITEM_MEASUREMENT_UNIT,
        "measurement_value": ITEM_MEASUREMENT_VALUE,
        "is_crucial": IS_CRUCIAL
    }

    item = SLAConfigurationItemController.create(**kwargs)

    ITEM_NEW_NAME = "New Test Item"
    ITEM_NEW_DESCRIPTION = "New Test Description"
    ITEM_NEW_VERSION = 2
    ITEM_NEW_SERVICE_TYPE = "New Test Service Type"
    ITEM_NEW_SERVICE_MANAGER = "New Test Service Manager"
    ITEM_NEW_CLIENT = "New Test Client"
    ITEM_NEW_STARTING_DATE = datetime.now()
    ITEM_NEW_ENDING_DATE = datetime.now()
    ITEM_NEW_MEASUREMENT_UNIT = "New Test Measurement Unit"
    ITEM_NEW_MEASUREMENT_VALUE = 20
    IS_NEW_CRUCIAL = False


    kwargs = {
        "name": ITEM_NEW_NAME,
        "description": ITEM_NEW_DESCRIPTION,
        "version": ITEM_NEW_VERSION,
        "service_type": ITEM_NEW_SERVICE_TYPE,
        "service_manager": ITEM_NEW_SERVICE_MANAGER,
        "client": ITEM_NEW_CLIENT,
        "starting_date": ITEM_NEW_STARTING_DATE,
        "ending_date": ITEM_NEW_ENDING_DATE,
        "measurement_unit": ITEM_NEW_MEASUREMENT_UNIT,
        "measurement_value": ITEM_NEW_MEASUREMENT_VALUE,
        "is_crucial": IS_NEW_CRUCIAL
    }

    item = SLAConfigurationItemController.update(item.id, **kwargs)

    assert item.name == ITEM_NEW_NAME
    assert item.description == ITEM_NEW_DESCRIPTION
    assert item.version == ITEM_NEW_VERSION
    assert item.service_type == ITEM_NEW_SERVICE_TYPE
    assert item.service_manager == ITEM_NEW_SERVICE_MANAGER
    assert item.client == ITEM_NEW_CLIENT
    assert item.starting_date == ITEM_NEW_STARTING_DATE
    assert item.ending_date == ITEM_NEW_ENDING_DATE
    assert item.measurement_unit == ITEM_NEW_MEASUREMENT_UNIT
    assert item.measurement_value == ITEM_NEW_MEASUREMENT_VALUE
    assert item.is_crucial == IS_NEW_CRUCIAL