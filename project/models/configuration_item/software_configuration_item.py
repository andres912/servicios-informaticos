from sqlalchemy import ForeignKey
from project.models.configuration_item.configuration_item import ConfigurationItem
from project import db


class SoftwareConfigurationItem(ConfigurationItem):
    __tablename__ = "ci_software"

    current_version_id = db.Column(db.Integer, ForeignKey("item_software_version.id"), nullable=True)
    # nullable True xq el ítem se crea antes que la primera versión
    draft_id = db.Column(db.Integer, ForeignKey("item_software_version.id"), nullable=True)
    versions = db.relationship("SoftwareItemVersion", backref="configuration_item", lazy=True, foreign_keys="SoftwareItemVersion.item_id")
    current_version = db.relationship("SoftwareItemVersion", foreign_keys=[current_version_id])
    draft = db.relationship("SoftwareItemVersion", foreign_keys=[draft_id])
    incidents = db.relationship("Incident", secondary="software_ci_item_incident")

    def __init__(self, current_version_id: int = None, **kwargs):
        super().__init__("Software")
        self.current_version_id = current_version_id
        self.draft_id = None

    
    