from project.controllers.solvable_controller import SolvableController
from project.models.comment import ProblemComment
from project.models.problem import Problem, NullProblem


class ProblemController(SolvableController):
    object_class = Problem
    null_object_class = NullProblem
    comment_class = ProblemComment

    @staticmethod
    def _verify_relations(problem: Problem) -> None:
        """
        Must be implemented.
        """
        pass
