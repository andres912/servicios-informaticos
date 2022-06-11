from project.controllers.solvable_controller import SolvableController
from project.models.comment import ChangeComment
from project.models.change import Change, NullChange
from project.models.association_tables.incident_change import IncidentChange
from project.models.association_tables.problem_change import ProblemChange


class ChangeController(SolvableController):
    object_class = Change
    null_object_class = NullChange
    comment_class = ChangeComment
