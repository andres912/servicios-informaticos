from project.controllers.solvable_controller import SolvableController
from project.helpers.link_creator import LinkCreator
from project.models.comment import IncidentComment, ProblemComment
from project.models.problem import Problem, NullProblem
from project import db


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


    @classmethod
    def create(cls, **kwargs):
        problem = super().create(**kwargs)
        for incident in problem.incidents:
            comment = IncidentComment(text=f"Se ha creado el problema con id {problem.id}, asociado a este incidente", object_id=incident.id)
            db.session.add(comment)
            LinkCreator.create_problem_details_link(comment, problem.id)
            
        db.session.commit()
        return problem