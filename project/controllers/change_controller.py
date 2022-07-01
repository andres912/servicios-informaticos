from project.controllers.configuration_item_controller.configuration_item_controller import (
    ConfigurationItemController,
)
from project.controllers.solvable_controller import SolvableController
from project.models.association_tables.configuration_item_incident import (
    HardwareConfigurationItemIncident,
)
from project.models.comment import (
    ChangeComment,
    HardwareItemComment,
    IncidentComment,
    ProblemComment,
    SLAItemComment,
    SoftwareItemComment,
)
from project.models.change import Change, NullChange
from project.models.association_tables.incident_change import IncidentChange
from project.models.association_tables.problem_change import ProblemChange
from project import db
from sqlalchemy import or_


class ChangeController(SolvableController):
    object_class = Change
    null_object_class = NullChange
    comment_class = ChangeComment

    @classmethod
    def apply_change(cls, change_id):
        change = cls.load_by_id(change_id)
        items = (
            change.hardware_configuration_items
            + change.software_configuration_items
            + change.sla_configuration_items
        )

        for item in items:
            if item.has_draft():
                next_version = item.last_version + 1
                cls.create_item_comment(item, change_id, next_version)
                item.apply_change(change_id)

        db.session.commit()
        return change

    @classmethod
    def discard_change(cls, change_id):
        change = cls.load_by_id(change_id)
        items = (
            change.hardware_configuration_items
            + change.software_configuration_items
            + change.sla_configuration_items
        )

        for item in items:
            if item.has_draft():
                draft = item.draft
                item.discard_change(change_id)

        db.session.commit()
        return change

    @classmethod
    def create(cls, **kwargs):
        change = super().create(**kwargs)
        for incident in change.incidents:
            comment = IncidentComment(
                text=f"Se ha creado el cambio con id {change.id}, asociado a este incidente",
                object_id=incident.id,
            )
            db.session.add(comment)
        for problem in change.problems:
            comment = ProblemComment(
                text=f"Se ha creado el cambio con id {change.id}, asociado a este problema",
                object_id=problem.id,
            )
            db.session.add(comment)
        db.session.commit()
        return change

    @classmethod
    def load_pending(cls):
        return cls.object_class.query.filter(
            or_(Change.status == "Pendiente", Change.status == "En proceso")
        ).all()

    @classmethod
    def create_item_comment(cls, item, change_id, version_number):
        item_type = item.item_type
        is_restoring_draft = item.draft.is_restoring_draft
        restored_version = item.get_restored_version_number()
        if item_type == "Hardware":
            if is_restoring_draft:
                comment = HardwareItemComment(
                    text=f"Se ha restaurado la versión {restored_version} del hardware a través del cambio {change_id}",
                    object_id=item.id,
                )
            else:
                comment = HardwareItemComment(
                    text=f"Se ha creado la versión {version_number} del ítem a través del cambio {change_id}",
                    object_id=item.id,
                )
        elif item_type == "Software":
            if is_restoring_draft:
                comment = SoftwareItemComment(
                    text=f"Se ha restaurado la versión {restored_version} del hardware a través del cambio {change_id}",
                    object_id=item.id,
                )
            else:
                comment = SoftwareItemComment(
                    text=f"Se ha creado la versión {version_number} del ítem a través del cambio {change_id}",
                    object_id=item.id,
                )
        elif item_type == "SLA":
            if is_restoring_draft:
                comment = SLAItemComment(
                    text=f"Se ha restaurado la versión {restored_version} del hardware a través del cambio {change_id}",
                    object_id=item.id,
                )
            else:
                comment = SLAItemComment(
                    text=f"Se ha creado la versión {version_number} del ítem a través del cambio {change_id}",
                    object_id=item.id,
                )
        db.session.add(comment)
        db.session.commit()
