from project.controllers.incident_controller import IncidentController
from project.controllers.problem_controller import ProblemController
from project.models.exceptions import ObjectNotFoundException

class ChangeRequestHelper:
    @classmethod
    def get_ci(cls, i, ci_hard, ci_sla, ci_soft):
        for cih in i.hardware_configuration_items:
            if not cih in ci_hard:
                ci_hard.append(cih)

        for cih in i.sla_configuration_items:
            if not cih in ci_sla:
                ci_sla.append(cih)

        for cih in i.software_configuration_items:
            if not cih in ci_soft:
                ci_soft.append(cih)


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
        incidents = {}

        problem_names = [
            raw_request[item] for item in raw_request if item.startswith("problem_name")
        ]
        problems_list = cls.get_problems(problem_names)
        for item in list(raw_request.keys()):
            if item.startswith("problem_name"):
                del raw_request[item]
            
        for p in problems_list:
            for i in p.incidents:
                if not i.name in incidents:
                    incidents[i.name] = i

        raw_request["problems"] = problems_list

        incident_names = [
            raw_request[item] for item in raw_request if item.startswith("incident_name")
        ]
        incidents_list = cls.get_incidents(incident_names)
        for item in list(raw_request.keys()):
            if item.startswith("incident_name"):
                del raw_request[item]
            
        raw_request["incidents"] = incidents_list

        ci_hard = []
        ci_sla = []
        ci_soft = []
        for i in incidents_list:
            cls.get_ci(i, ci_hard, ci_sla, ci_soft)

        for _,i in incidents.items():
            cls.get_ci(i, ci_hard, ci_sla, ci_soft)

        raw_request["sla_configuration_items"] = ci_sla
        raw_request["software_configuration_items"] = ci_soft
        raw_request["hardware_configuration_items"] = ci_hard
        return raw_request

