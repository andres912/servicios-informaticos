from datetime import datetime
from project.models.versions.software_item_version import (
    SoftwareItemVersion,
)
from project.models.priority import PRIORITY_MEDIUM


def test_software_configuration_item_creation(init_database, saved_user, saved_hardware_configuration_item):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_TYPE = "Test Type"
    ITEM_PROVIDER = "Test Provider"
    ITEM_SOFTWARE_VERSION = "10.0.0"
    ITEM_ID = saved_hardware_configuration_item.id

    item = SoftwareItemVersion(
        name=ITEM_NAME,
        description=ITEM_DESCRIPTION,
        type=ITEM_TYPE,
        provider=ITEM_PROVIDER,
        software_version=ITEM_SOFTWARE_VERSION,
        item_id=ITEM_ID,
    )

    assert item.name == ITEM_NAME
    assert item.description == ITEM_DESCRIPTION
    assert item.type == ITEM_TYPE
    assert item.provider == ITEM_PROVIDER
    assert item.software_version == ITEM_SOFTWARE_VERSION


def test_software_configuration_item_update(init_database, saved_user, saved_hardware_configuration_item):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_TYPE = "Test Type"
    ITEM_PROVIDER = "Test Provider"
    ITEM_SOFTWARE_VERSION = "10.0.0"
    ITEM_ID = saved_hardware_configuration_item.id

    item = SoftwareItemVersion(
        name=ITEM_NAME,
        description=ITEM_DESCRIPTION,
        type=ITEM_TYPE,
        provider=ITEM_PROVIDER,
        software_version=ITEM_SOFTWARE_VERSION,
        item_id=ITEM_ID,
    )

    ITEM_NEW_NAME = "New Test Item"
    ITEM_NEW_DESCRIPTION = "New Test Description"
    ITEM_NEW_TYPE = "New Test Type"
    ITEM_NEW_PROVIDER = "New Test Provider"
    ITEM_NEW_SOFTWARE_VERSION = "11.0.0"

    item.update(
        name=ITEM_NEW_NAME,
        description=ITEM_NEW_DESCRIPTION,
        type=ITEM_NEW_TYPE,
        provider=ITEM_NEW_PROVIDER,
        software_version=ITEM_NEW_SOFTWARE_VERSION,
    )

    assert item.name == ITEM_NEW_NAME
    assert item.description == ITEM_NEW_DESCRIPTION
    assert item.type == ITEM_NEW_TYPE
    assert item.provider == ITEM_NEW_PROVIDER
    assert item.software_version == ITEM_NEW_SOFTWARE_VERSION

