from flask import Blueprint, jsonify, request

PROBLEMS_ENDPOINT = "/problems"

problem_blueprint = Blueprint("problem_blueprint", __name__)
