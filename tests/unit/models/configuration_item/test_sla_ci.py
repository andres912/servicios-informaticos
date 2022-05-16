from datetime import datetime
from project.models.configuration_item.sla_configuration_item import (
    SLAConfigurationItem,
)
from project.models.priority import PRIORITY_MEDIUM


def test_SLA_configuration_item_creation(init_database, saved_user):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_FAMILY_ITEM_ID = 1
    ITEM_SERVICE_TYPE = "Test Service Type"
    ITEM_SERVICE_MANAGER = "Test Service Manager"
    ITEM_CLIENT = "Test Client"
    ITEM_STARTING_DATE = datetime.now()
    ITEM_ENDING_DATE = datetime.now()
    ITEM_MEASUREMENT_UNIT = "Test Measurement Unit"
    ITEM_MEASUREMENT_VALUE = 10

    item = SLAConfigurationItem(
        name=ITEM_NAME,
        description=ITEM_DESCRIPTION,
        item_family_id=ITEM_FAMILY_ITEM_ID,
        version=ITEM_VERSION,
        service_type=ITEM_SERVICE_TYPE,
        service_manager=ITEM_SERVICE_MANAGER,
        client=ITEM_CLIENT,
        starting_date=ITEM_STARTING_DATE,
        ending_date=ITEM_ENDING_DATE,
        measurement_unit=ITEM_MEASUREMENT_UNIT,
        measurement_value=ITEM_MEASUREMENT_VALUE,
    )

    assert item.name == ITEM_NAME
    assert item.description == ITEM_DESCRIPTION
    assert item.item_family_id == ITEM_FAMILY_ITEM_ID
    assert item.version == ITEM_VERSION
    assert item.service_type == ITEM_SERVICE_TYPE
    assert item.service_manager == ITEM_SERVICE_MANAGER
    assert item.client == ITEM_CLIENT
    assert item.starting_date == ITEM_STARTING_DATE
    assert item.ending_date == ITEM_ENDING_DATE
    assert item.measurement_unit == ITEM_MEASUREMENT_UNIT
    assert item.measurement_value == ITEM_MEASUREMENT_VALUE
    assert item.item_class == "SLA"


def test_software_configuration_item_update(init_database, saved_user):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_FAMILY_ITEM_ID = 1
    ITEM_SERVICE_TYPE = "Test Service Type"
    ITEM_SERVICE_MANAGER = "Test Service Manager"
    ITEM_CLIENT = "Test Client"
    ITEM_STARTING_DATE = datetime.now()
    ITEM_ENDING_DATE = datetime.now()
    ITEM_MEASUREMENT_UNIT = "Test Measurement Unit"
    ITEM_MEASUREMENT_VALUE = 10

    item = SLAConfigurationItem(
        name=ITEM_NAME,
        description=ITEM_DESCRIPTION,
        item_family_id=ITEM_FAMILY_ITEM_ID,
        version=ITEM_VERSION,
        service_type=ITEM_SERVICE_TYPE,
        service_manager=ITEM_SERVICE_MANAGER,
        client=ITEM_CLIENT,
        starting_date=ITEM_STARTING_DATE,
        ending_date=ITEM_ENDING_DATE,
        measurement_unit=ITEM_MEASUREMENT_UNIT,
        measurement_value=ITEM_MEASUREMENT_VALUE,
    )

    starting_date = datetime.now()
    ending_date = datetime.now()

    ITEM_NEW_NAME = "New Test Item"
    ITEM_NEW_DESCRIPTION = "New Test Description"
    ITEM_NEW_VERSION = 2
    ITEM_NEW_ID = 2
    ITEM_NEW_SERVICE_TYPE = "New Test Service Type"
    ITEM_NEW_SERVICE_MANAGER = "New Test Service Manager"
    ITEM_NEW_CLIENT = "New Test Client"
    ITEM_NEW_STARTING_DATE = starting_date
    ITEM_NEW_ENDING_DATE = ending_date
    ITEM_NEW_MEASUREMENT_UNIT = "New Test Measurement Unit"
    ITEM_NEW_MEASUREMENT_VALUE = 20

    item.update(
        name=ITEM_NEW_NAME,
        description=ITEM_NEW_DESCRIPTION,
        version=ITEM_NEW_VERSION,
        item_family_id=ITEM_NEW_ID,
        service_type=ITEM_NEW_SERVICE_TYPE,
        service_manager=ITEM_NEW_SERVICE_MANAGER,
        client=ITEM_NEW_CLIENT,
        starting_date=ITEM_NEW_STARTING_DATE,
        ending_date=ITEM_NEW_ENDING_DATE,
        measurement_unit=ITEM_NEW_MEASUREMENT_UNIT,
        measurement_value=ITEM_NEW_MEASUREMENT_VALUE,
    )

    assert item.name == ITEM_NEW_NAME
    assert item.description == ITEM_NEW_DESCRIPTION
    assert item.version == ITEM_NEW_VERSION
    assert item.item_family_id == ITEM_NEW_ID
    assert item.service_type == ITEM_NEW_SERVICE_TYPE
    assert item.service_manager == ITEM_NEW_SERVICE_MANAGER
    assert item.client == ITEM_NEW_CLIENT
    assert item.starting_date == ITEM_NEW_STARTING_DATE
    assert item.ending_date == ITEM_NEW_ENDING_DATE
    assert item.measurement_unit == ITEM_NEW_MEASUREMENT_UNIT
    assert item.measurement_value == ITEM_NEW_MEASUREMENT_VALUE
