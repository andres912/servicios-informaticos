from flask import Blueprint, jsonify, request

CHANGES_ENDPOINT = "/changes"

change_blueprint = Blueprint("change_blueprint", __name__)