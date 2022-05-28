from flask import Blueprint, jsonify, request
from project.controllers.problem_controller import ProblemController
from project.schemas.schemas import ProblemSchema

PROBLEMS_ENDPOINT = "/problems"

problem_blueprint = Blueprint("problem_blueprint", __name__)

problem_schema = ProblemSchema()
problems_schema = ProblemSchema(many=True)


@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_problems():
    """
    GET endpoint to get all Problems.
    """
    problems = ProblemController.load_all()
    return jsonify(problems_schema.dump(problems))

@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}/<user_id>", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_user_problems(user_id):
    """
    GET endpoint to get all Problems from a specific user.
    """
    problems = ProblemController.load_problems_assigned_to_user(username=user_id)
    return jsonify(problems_schema.dump(problems))

@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}/assigned", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_assigned_problems():
    """
    GET endpoint to get all Problems.
    """
    problems = ProblemController.load_assigned_problems()
    return jsonify(problems_schema.dump(problems))

@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}/not-assigned", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_unassigned_problems():
    """
    GET endpoint to get all Problems.
    """
    problems = ProblemController.load_unassigned_problems()
    return jsonify(problems_schema.dump(problems))


@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}", methods=["POST"])
# @user_required([EDIT_DISTRIBUTOR])
def create_problem():
    """
    POST endpoint to create a new Problem.
    """
    #new_problem = problem_schema.load(request.json)
    problem = ProblemController.create(**request.json)
    return problem_schema.dump(problem)


@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}/<problem_id>", methods=["DELETE"])
# @user_required([EDIT_DISTRIBUTOR])
def delete_problem(problem_id):
    """
    DELETE endpoint to delete a given Problem.
    """
    problem = ProblemController.load_by_id(problem_id)
    try:
        ProblemController.delete(problem)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@problem_blueprint.route(f"{PROBLEMS_ENDPOINT}/all", methods=["DELETE"])
# @user_required([EDIT_DISTRIBUTOR])
def delete_all():
    """
    DELETE endpoint to delete all Problems.
    """
    problems_amount = ProblemController.count()
    ProblemController.delete_all()
    return f"{problems_amount} problems have been deleted"
