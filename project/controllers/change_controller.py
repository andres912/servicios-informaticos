from project.controllers.configuration_item_controller.configuration_item_controller import ConfigurationItemController
from project.controllers.solvable_controller import SolvableController
from project.models.comment import ChangeComment
from project.models.change import Change, NullChange
from project.models.association_tables.incident_change import IncidentChange
from project.models.association_tables.problem_change import ProblemChange
from project import db


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
