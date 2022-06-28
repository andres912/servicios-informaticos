from datetime import datetime
from project.models.versions.hardware_item_version import HardwareItemVersion
from project.models.versions.sla_item_version import SLAItemVersion
from project.models.versions.software_item_version import SoftwareItemVersion


class ItemHelper:
    
    @classmethod
    def create_restore_draft(cls, item, change_id, restore_version_id):
        item_type = item.item_type
        item_id = item.id

        if item_type == "Software":
            return cls.create_software_restore_draft(item_id, change_id, restore_version_id)
        elif item_type == "Hardware":
            return cls.create_hardware_restore_draft(item_id, change_id, restore_version_id)
        elif item_type == "SLA":
            return cls.create_sla_restore_draft(item_id, change_id, restore_version_id)
        else:
            raise Exception("Item type not supported")


    @classmethod
    def create_software_restore_draft(cls, item_id, change_id, restore_version_id):
        restore_draft = SoftwareItemVersion(
            item_id=item_id,
            name="Restore",
            description="Restore",
            version_number=0,
            is_draft=True,
            is_restoring_draft=True,
            restore_version_id=restore_version_id,
            provider="Restore",
            software_version="Restore",
            type="Restore"
        )
        restore_draft.change_id = change_id
        return restore_draft

    @classmethod
    def create_hardware_restore_draft(cls, item_id, change_id, restore_version_id):
        restore_draft = HardwareItemVersion(
            item_id=item_id,
            name="Restore",
            description="Restore",
            version_number=0,
            is_draft=True,
            is_restoring_draft=True,
            restore_version_id=restore_version_id,
            manufacturer="Restore",
            type="Restore",
            serial_number="Restore",
            price=0,
            purchase_date=datetime.now()
        )
        restore_draft.change_id = change_id
        return restore_draft

    @classmethod
    def create_sla_restore_draft(cls, item_id, change_id, restore_version_id):
        restore_draft = SLAItemVersion(
            item_id=item_id,
            name="Restore",
            description="Restore",
            version_number=0,
            is_draft=True,
            is_restoring_draft=True,
            restore_version_id=restore_version_id,
            service_type="Restore",
            service_manager="Restore",
            client="Restore",
            starting_date=datetime.now(),
            ending_date=datetime.now(),
            measuremente_unit="Restore",
            measurement_value=0,
            is_crucial=False
        )
        restore_draft.change_id = change_id
        return restore_draft