from sqlalchemy import ForeignKey
from project.models.exceptions import ChangeApplicationError, ObjectCreationException
from project.models.versions.hardware_item_version import HardwareItemVersion
from project.models.versions.software_item_version import SoftwareItemVersion
from project.models.versions.sla_item_version import SLAItemVersion
from project.models.versions.item_version import ItemVersion
from project.models.base_model import BaseModel
from project import db
from project.models.association_tables.configuration_item_incident import (
    HardwareConfigurationItemIncident,
)
from project.models.association_tables.configuration_item_incident import (
    SoftwareConfigurationItemIncident,
)
from project.models.association_tables.configuration_item_incident import (
    SLAConfigurationItemIncident,
)

class ConfigurationItem(BaseModel):
    __abstract__ = True

    item_type = db.Column(db.String(20), nullable=False)
    last_version = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, item_type: str, **kwargs):
        self.item_type = item_type
        self.last_version = 1

    def update(self, **kwargs):
        return self.current_version.update(**kwargs)

    def set_current_version(self, version_id: int):
        self.current_version_id = version_id

    def set_draft(self, version_id: int):
        self.draft_id = version_id

    def has_draft(self):
        return self.draft_id is not None

    def get_versions(self):
        versions = self.versions
        for version in versions:
            if version.id == self.curent_version_id or version.is_draft:
                versions.remove(version)
        return versions

    def apply_change(self, change_id):
        draft = self.draft
        if change_id != draft.change_id:
            raise ChangeApplicationError(item_id=self.id, change_id=change_id)

        if draft.is_restoring_draft:
            self.restore_version(draft)
            return

        self.current_version_id = draft.id
        self.draft.is_draft = False
        self.draft_id = None
        self.last_version += 1
        self.draft.version_number = self.last_version

    def discard_change(self, change_id):
        draft = self.draft
        if change_id != draft.change_id:
            raise ChangeApplicationError(item_id=self.id, change_id=change_id)

        self.draft_id = None
        self.draft = None
        db.session.commit()
        draft.force_delete()

    def restore_version(self, draft):
        version_id = draft.restore_version_id
        self.current_version_id = version_id
        self.draft_id = None
        db.session.commit()
        draft.force_delete()

    def get_restored_version_number(self):
        restored_version_id = self.draft.restore_version_id
        restored_version = list(filter(lambda version: version.id == restored_version_id, self.versions))[0]
        return restored_version.version_number
