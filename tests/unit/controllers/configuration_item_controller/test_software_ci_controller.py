from datetime import datetime
from project.controllers.configuration_item_controller.software_ci_controller import SoftwareConfigurationItemController
from project import db


def test_hardware_ci_item_creation(init_database):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_TYPE = "Test Type"
    ITEM_PROVIDER = "Test Provider"
    ITEM_SOFTWARE_VERSION = "10.0.0"

    kwargs = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "version": ITEM_VERSION,
        "type": ITEM_TYPE,
        "provider": ITEM_PROVIDER,
        "software_version": ITEM_SOFTWARE_VERSION,
    }


    item = SoftwareConfigurationItemController.create(**kwargs)

    assert item.name == ITEM_NAME
    assert item.description == ITEM_DESCRIPTION
    assert item.version == ITEM_VERSION
    assert item.type == ITEM_TYPE
    assert item.provider == ITEM_PROVIDER
    assert item.software_version == ITEM_SOFTWARE_VERSION

def test_hardware_ci_item_update(init_database):

    ITEM_NAME = "Test Item"
    ITEM_DESCRIPTION = "Test Description"
    ITEM_VERSION = 1
    ITEM_TYPE = "Test Type"
    ITEM_PROVIDER = "Test Provider"
    ITEM_SOFTWARE_VERSION = "10.0.0"

    kwargs = {
        "name": ITEM_NAME,
        "description": ITEM_DESCRIPTION,
        "version": ITEM_VERSION,
        "type": ITEM_TYPE,
        "provider": ITEM_PROVIDER,
        "software_version": ITEM_SOFTWARE_VERSION,
    }

    item = SoftwareConfigurationItemController.create(**kwargs)

    ITEM_NEW_NAME = "New Test Item"
    ITEM_NEW_DESCRIPTION = "New Test Description"
    ITEM_NEW_VERSION = 2
    ITEM_NEW_TYPE = "New Test Type"
    ITEM_NEW_PROVIDER = "New Test Provider"
    ITEM_NEW_SOFTWARE_VERSION = "10.0.1"

    kwargs = {
        "name": ITEM_NEW_NAME,
        "description": ITEM_NEW_DESCRIPTION,
        "version": ITEM_NEW_VERSION,
        "type": ITEM_NEW_TYPE,
        "provider": ITEM_NEW_PROVIDER,
        "software_version": ITEM_NEW_SOFTWARE_VERSION,
    }

    item = SoftwareConfigurationItemController.update(item.id, **kwargs)

    assert item.name == ITEM_NEW_NAME
    assert item.description == ITEM_NEW_DESCRIPTION
    assert item.version == ITEM_NEW_VERSION
    assert item.type == ITEM_NEW_TYPE
    assert item.provider == ITEM_NEW_PROVIDER
    assert item.software_version == ITEM_NEW_SOFTWARE_VERSION