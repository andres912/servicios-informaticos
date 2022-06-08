class ChangeRequestHelper:
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

