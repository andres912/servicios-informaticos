from flask import Blueprint

HEALTH_ENDPOINT = "/"

health_blueprint = Blueprint("health_blueprint", __name__)


@health_blueprint.route(HEALTH_ENDPOINT, methods=["GET"])
def get_helth():
    """Used by AWS Elastic Load Balancing health checks"""
    return "Health is ok!", 200
