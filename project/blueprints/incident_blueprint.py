from flask import Blueprint, jsonify, request
from project.controllers.incident_controller import IncidentController
from project.controllers.user_controller import UserController
from project.schemas.schemas import AlternativeIncidentSchema, IncidentSchema
from project.helpers.incident_request_helper import IncidentRequestHelper

INCIDENTS_ENDPOINT = "/incidents"

incident_blueprint = Blueprint("incidents_blueprint", __name__)
incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)
alternative_incident_schema = AlternativeIncidentSchema()
alternative_incidents_schema = AlternativeIncidentSchema(many=True)
reduced_incidents_schema = IncidentSchema(many=True, only=["description"])


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_incidents():
    """
    GET endpoint to get all Incidents.
    """
    incidents = IncidentController.load_all()
    return jsonify(alternative_incidents_schema.dump(incidents))


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/<incident_id>", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_incident(incident_id):
    """
    GET endpoint to get an Incident.
    """
    try:
        incident = IncidentController.load_by_id(incident_id)
        return alternative_incident_schema.dump(incident), 200
    except Exception as e:
        return jsonify({"error": e.message}), 404


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/assigned", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_assigned_incidents():
    """
    GET endpoint to get all Incidents.
    """
    incidents = IncidentController.load_assigned()
    return jsonify(incidents_schema.dump(incidents))


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/not-assigned", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_unassigned_incidents():
    """
    GET endpoint to get all Incidents.
    """
    incidents = IncidentController.load_unassigned()
    return jsonify(incidents_schema.dump(incidents))


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/solved", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_solved_incidents():
    """
    GET endpoint to get all Incidents.
    """
    incidents = IncidentController.load_solved()
    return jsonify(incidents_schema.dump(incidents))


@incident_blueprint.route(f"/users/<user_id>{INCIDENTS_ENDPOINT}", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_user_incidents(user_id):
    """
    GET endpoint to get all Incidents.
    """
    try:
        username = UserController.load_by_id(user_id).username
        incidents = IncidentController.load_taken_by_user(username)
        return jsonify(incidents_schema.dump(incidents))
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}", methods=["POST"])
# @user_required([EDIT_DISTRIBUTOR])
def create_incident():
    """
    POST endpoint to create a new Incident.
    """
    correct_request = IncidentRequestHelper.create_incident_request(request.json)
    incident = IncidentController.create(**correct_request)
    return incident_schema.dump(incident)


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/<incident_id>", methods=["DELETE"])
# @user_required([EDIT_DISTRIBUTOR])
def delete_incident(incident_id):
    """
    DELETE endpoint to delete a given Incident.
    """
    incident = IncidentController.load_by_id(incident_id)
    try:
        IncidentController.delete(incident)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/all", methods=["DELETE"])
# @user_required([EDIT_DISTRIBUTOR])
def delete_all():
    """
    DELETE endpoint to delete all Incidents.
    """
    incidents_amount = IncidentController.count()
    IncidentController.delete_all()
    return f"{incidents_amount} incidents have been deleted"


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/<incident_id>", methods=["PATCH"])
# @user_required([EDIT_DISTRIBUTOR])
def update_incident(incident_id):
    """
    POST endpoint to create a new Incident.
    """
    incident = IncidentController.update(id=incident_id, **request.json)
    return jsonify(incident_schema.dump(incident))


@incident_blueprint.route(f"{INCIDENTS_ENDPOINT}/names", methods=["GET"])
# @user_required([EDIT_DISTRIBUTOR])
def get_incidents_names():
    """
    GET endpoint to get incidents names
    """
    incidents = IncidentController.load_unresolved()
    response = {
        "incidents": [
            {"value": incident.description, "label": incident.description}
            for incident in incidents
        ]
    }
    return jsonify(response)


@incident_blueprint.route(
    f"{INCIDENTS_ENDPOINT}/<incident_id>/comments", methods=["POST"]
)
# @user_required([EDIT_DISTRIBUTOR])
def add_comment_to_incident(incident_id):
    """
    GET endpoint to get incidents names
    """
    comment = request.json["comment"]
    created_by = request.json["created_by"]
    IncidentController.add_comment_to_solvable(
        solvable_id=incident_id, comment_message=comment, created_by=created_by
    )
    return jsonify({"message": "Comment added"})
