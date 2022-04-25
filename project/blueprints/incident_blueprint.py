from flask import Blueprint, jsonify, request
from project.controllers.incident_controller import IncidentController
from project.schemas.schemas import IncidentSchema

INCIDENTS_ENDPOINT = "/incidents"

incident_blueprint = Blueprint("incidents_blueprint", __name__)
incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_incidents():
    """
    GET endpoint to get all Incidents.
    """
    incidents = IncidentController.load_all()
    return jsonify(incidents_schema.dump(incidents))


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}", methods=["POST"])
# @user_required([EDIT_DISTRIBUTOR])
def create_incident():
    """
    POST endpoint to create a new Incident.
    """
    new_incident = incident_schema.load(request.json)
    IncidentController.save(new_incident)
    return incident_schema.dump(new_incident)


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}", methods=["DELETE"])
# @user_required([EDIT_DISTRIBUTOR])
def delete_incident():
    """
    DELETE endpoint to delete a given Incident.
    """
    return "Method not implemented", 200
