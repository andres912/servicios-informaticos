from sqlalchemy import ForeignKey
from project.models.comment import HardwareItemComment
from project.models.configuration_item.configuration_item import ConfigurationItem
from project import db
from project.models.versions.hardware_item_version import HardwareItemVersion


class HardwareConfigurationItem(ConfigurationItem):
    __tablename__ = "ci_hardware"
    comment_class = HardwareItemComment

    current_version_id = db.Column(
        db.Integer, ForeignKey("item_hardware_version.id"), nullable=True
    )
    # nullable True xq el ítem se crea antes que la primera versión
    draft_id = db.Column(
        db.Integer, ForeignKey("item_hardware_version.id"), nullable=True
    )
    versions = db.relationship(
        "HardwareItemVersion",
        foreign_keys="HardwareItemVersion.item_id",
        cascade="all, delete-orphan",
    )
    current_version = db.relationship(
        "HardwareItemVersion", foreign_keys=[current_version_id]
    )
    draft = db.relationship("HardwareItemVersion", foreign_keys=[draft_id])
    incidents = db.relationship("Incident", secondary="hardware_ci_item_incident")
    comments = db.relationship("HardwareItemComment", lazy="dynamic")

    def __init__(self, current_version_id: int = None, **kwargs):
        super().__init__("Hardware")
        self.current_version_id = current_version_id
        self.draft_id = None

