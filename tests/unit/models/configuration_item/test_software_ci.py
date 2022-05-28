from datetime import datetime
from project.models.configuration_item.software_configuration_item import (
    SoftwareConfigurationItem,
)
from project.models.priority import PRIORITY_MEDIUM


def test_software_configuration_item_creation(init_database, saved_user):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_FAMILY_ITEM_ID = 1
    ITEM_TYPE = "Test Type"
    ITEM_PROVIDER = "Test Provider"
    ITEM_SOFTWARE_VERSION = "10.0.0"

    item = SoftwareConfigurationItem(
        name=ITEM_NAME,
        description=ITEM_DESCRIPTION,
        item_family_id=ITEM_FAMILY_ITEM_ID,
        version=ITEM_VERSION,
        type=ITEM_TYPE,
        provider=ITEM_PROVIDER,
        software_version=ITEM_SOFTWARE_VERSION,
    )

    assert item.name == ITEM_NAME
    assert item.description == ITEM_DESCRIPTION
    assert item.item_family_id == ITEM_FAMILY_ITEM_ID
    assert item.version == ITEM_VERSION
    assert item.type == ITEM_TYPE
    assert item.provider == ITEM_PROVIDER
    assert item.software_version == ITEM_SOFTWARE_VERSION
    assert item.item_class == "Software"


def test_software_configuration_item_update(init_database, saved_user):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_FAMILY_ITEM_ID = 1
    ITEM_TYPE = "Test Type"
    ITEM_PROVIDER = "Test Provider"
    ITEM_SOFTWARE_VERSION = "10.0.0"

    item = SoftwareConfigurationItem(
        name=ITEM_NAME,
        description=ITEM_DESCRIPTION,
        item_family_id=ITEM_FAMILY_ITEM_ID,
        version=ITEM_VERSION,
        type=ITEM_TYPE,
        provider=ITEM_PROVIDER,
        software_version=ITEM_SOFTWARE_VERSION,
    )

    ITEM_NEW_NAME = "New Test Item"
    ITEM_NEW_DESCRIPTION = "New Test Description"
    ITEM_NEW_VERSION = 2
    ITEM_NEW_ID = 2
    ITEM_NEW_TYPE = "New Test Type"
    ITEM_NEW_PROVIDER = "New Test Provider"
    ITEM_NEW_SOFTWARE_VERSION = "11.0.0"

    item.update(
        name=ITEM_NEW_NAME,
        description=ITEM_NEW_DESCRIPTION,
        version=ITEM_NEW_VERSION,
        item_family_id=ITEM_NEW_ID,
        type=ITEM_NEW_TYPE,
        provider=ITEM_NEW_PROVIDER,
        software_version=ITEM_NEW_SOFTWARE_VERSION,
    )

    assert item.name == ITEM_NEW_NAME
    assert item.description == ITEM_NEW_DESCRIPTION
    assert item.version == ITEM_NEW_VERSION
    assert item.item_family_id == ITEM_NEW_ID
    assert item.type == ITEM_NEW_TYPE
    assert item.provider == ITEM_NEW_PROVIDER
    assert item.software_version == ITEM_NEW_SOFTWARE_VERSION
