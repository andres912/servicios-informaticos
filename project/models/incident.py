from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.status import *
from project.models.association_tables.configuration_item_incident import HardwareConfigurationItemIncident
from project.models.association_tables.configuration_item_incident import SoftwareConfigurationItemIncident
from project.models.association_tables.configuration_item_incident import SLAConfigurationItemIncident


class Incident(BaseModel):
    __tablename__ = "incident"
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20))
    created_by = db.Column(db.String(30), db.ForeignKey("user.username"))
    taken_by = db.Column(db.String(30), db.ForeignKey("user.username"))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    hardware_configuration_items = db.relationship("HardwareConfigurationItem", secondary="hardware_ci_item_incident")
    software_configuration_items = db.relationship("SoftwareConfigurationItem", secondary="software_ci_item_incident")
    sla_configuration_items = db.relationship("SLAConfigurationItem", secondary="sla_ci_item_incident")
    is_blocked = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        description: str,
        priority: str = PRIORITY_MEDIUM,
        created_by: str = "",
        hardware_configuration_items: list = [],
        software_configuration_items: list = [],
        sla_configuration_items: list = [],
    ):
        self.verify_items(hardware_configuration_items, software_configuration_items, sla_configuration_items)
        self.description = description
        self.priority = priority
        self.created_by = created_by
        self.hardware_configuration_items = hardware_configuration_items
        self.software_configuration_items = software_configuration_items
        self.sla_configuration_items = sla_configuration_items
        self.status = STATUS_PENDING
        self.taken_by = None
        self.is_blocked = False


    def _update(self,
                title: str = None,
                description: str = None,
                priority: str = None,
                status: str = None,
                taken_by: str = None,
                is_blocked: bool = None) -> None:
        if title:
            self.title = title
        if description:
            self.description = description
        if priority:
            self.priority = priority
        if status:
            self.status = status
        if taken_by:
            self.taken_by = taken_by
        if is_blocked != None:
            self.is_blocked = is_blocked

    def change_status(self, status: str) -> None:
        self._update(self, status=status)

    def change_priority(self, priority: str) -> None:
        self._update(self, priority=priority)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)

    def verify_items(self, hardware_configuration_items: list, software_configuration_items: list, sla_configuration_items: list) -> None:
        if not hardware_configuration_items and not software_configuration_items and not sla_configuration_items:
            raise ObjectCreationException(object="Incident", cause="No configuration items provided")

class NullIncident(NullBaseModel, Incident):
    __abstract__ = True
