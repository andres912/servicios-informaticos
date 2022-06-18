from project import db
from project.models.base_model import BaseModel, NullBaseModel
from project.models.exceptions import ObjectCreationException
from project.models.priority import *
from project.models.solvable import Solvable
from project.models.status import *
from project.models.comment import ChangeComment
from project.models.incident import Incident
from project.models.problem import Problem

from project.models.association_tables.configuration_item_change import (
    HardwareConfigurationItemChange,
)
from project.models.association_tables.configuration_item_change import (
    SoftwareConfigurationItemChange,
)
from project.models.association_tables.configuration_item_change import (
    SLAConfigurationItemChange,
)

class Change(Solvable):
    __tablename__ = "change"
    incidents = db.relationship("Incident", secondary="incident_change")
    problems = db.relationship("Problem", secondary="problem_change")

    hardware_configuration_items = db.relationship(
        "HardwareConfigurationItem", secondary="hardware_ci_item_change"
    )
    software_configuration_items = db.relationship(
        "SoftwareConfigurationItem", secondary="software_ci_item_change"
    )
    sla_configuration_items = db.relationship(
        "SLAConfigurationItem", secondary="sla_ci_item_change"
    )

    comments = db.relationship("ChangeComment", backref="change", lazy="dynamic")

    def __init__(
        self,
        incidents: list = [],
        problems: list = [],
        hardware_configuration_items: list = [],
        software_configuration_items: list = [],
        sla_configuration_items: list = [],
        **kwargs
    ):
        self.incidents = incidents
        self.problems = problems
        super().__init__(**kwargs)
        self.verify_items(
            hardware_configuration_items,
            software_configuration_items,
            sla_configuration_items,
        )
        self.hardware_configuration_items = hardware_configuration_items
        self.software_configuration_items = software_configuration_items
        self.sla_configuration_items = sla_configuration_items

    def verify_items(
        self,
        hardware_configuration_items: list,
        software_configuration_items: list,
        sla_configuration_items: list,
    ) -> None:
        if (
            not hardware_configuration_items
            and not software_configuration_items
            and not sla_configuration_items
        ):
            raise ObjectCreationException(
                object="Incident", cause="No configuration items provided"
            )


    def _update(
        self,
        title: str = None,
        description: str = None,
        priority: str = None,
        status: str = None,
        taken_by: str = None,
    ) -> None:
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

    def change_status(self, status: str) -> None:
        self._update(self, status=status)

    def change_priority(self, priority: str) -> None:
        self._update(self, priority=priority)

    def assign_user(self, taken_by: str) -> None:
        self._update(self, taken_by=taken_by)
    
    def verify_problems_incidents(self, incidents: list, problems: list) -> None:
        if not problems and not incidents:
            raise ObjectCreationException(
                object="Change", cause="Requires atleast 1 incident OR problem"
            )



class NullChange(NullBaseModel, Change):
    __abstract__ = True
