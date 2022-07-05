from sqlalchemy import ForeignKey
from project.models.comment import SLAItemComment
from project.models.configuration_item.configuration_item import ConfigurationItem
from project import db
from project.models.versions.sla_item_version import SLAItemVersion


class SLAConfigurationItem(ConfigurationItem):
    __tablename__ = "ci_sla"
    comment_class = SLAItemComment

    current_version_id = db.Column(db.Integer, ForeignKey("item_sla_version.id"), nullable=True)
    # nullable True xq el ítem se crea antes que la primera versión
    draft_id = db.Column(db.Integer, ForeignKey("item_sla_version.id"), nullable=True)
    versions = db.relationship("SLAItemVersion", backref="configuration_item", lazy=True, foreign_keys="SLAItemVersion.item_id")
    current_version = db.relationship("SLAItemVersion", foreign_keys=[current_version_id])
    draft = db.relationship("SLAItemVersion", foreign_keys=[draft_id])
    incidents = db.relationship("Incident", secondary="sla_ci_item_incident")
    comments = db.relationship("SLAItemComment", lazy="dynamic")
    changes = db.relationship("Change", secondary="sla_ci_item_change")

    def __init__(self, current_version_id: int = None, **kwargs):
        super().__init__("SLA")
        self.current_version_id = current_version_id
        self.draft_id = None