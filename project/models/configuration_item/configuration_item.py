from sqlalchemy import ForeignKey
from project.models.versions.hardware_item_version import HardwareItemVersion
from project.models.versions.software_item_version import SoftwareItemVersion
from project.models.versions.sla_item_version import SLAItemVersion
from project.models.versions.item_version import ItemVersion
from project.models.base_model import BaseModel
from project import db


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