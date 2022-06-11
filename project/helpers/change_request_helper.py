from project.controllers.incident_controller import IncidentController
from project.controllers.problem_controller import ProblemController

class ChangeRequestHelper:
    @classmethod
    def get_incidents(cls, incident_names):
        """
        Get all configuration items by name
        """
        incidents_list = []
        for incident_name in incident_names:
            incident = IncidentController.load_by_description(incident_name)
            if not incident:
                raise ObjectNotFoundException()
            incidents_list.append(incident)
        return incidents_list

    @classmethod
    def get_problems(cls, problem_names):
        """
        Get all configuration items by name
        """
        incidents_list = []
        for incident_name in problem_names:
            incident = ProblemController.load_by_description(incident_name)
            if not incident:
                raise ObjectNotFoundException()
            incidents_list.append(incident)
        return incidents_list

    @classmethod
    def create_change_request(cls, raw_request):
        problem_names = [
            raw_request[item] for item in raw_request if item.startswith("problem_name")
        ]
        problems_list = cls.get_problems(problem_names)
        for item in list(raw_request.keys()):
            if item.startswith("problem_name"):
                del raw_request[item]
            
        raw_request["problems"] = problems_list

        incident_names = [
            raw_request[item] for item in raw_request if item.startswith("incident_name")
        ]
        incidents_list = cls.get_incidents(incident_names)
        for item in list(raw_request.keys()):
            if item.startswith("incident_name"):
                del raw_request[item]
            
        raw_request["incidents"] = incidents_list
        return raw_request

