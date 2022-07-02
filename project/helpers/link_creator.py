class LinkCreator():
    
    @classmethod
    def create_change_details_link(cls, comment, change_id):
        comment.has_link = True
        comment.link_url = f"/change_details/{change_id}"
        comment.link_text = "ver cambio"

    @classmethod
    def create_problem_details_link(cls, comment, problem_id):
        comment.has_link = True
        comment.link_url = f"/problem_details/{problem_id}"
        comment.link_text = "ver problema"

    @classmethod
    def create_incident_details_link(cls, comment, incident_id):
        comment.has_link = True
        comment.link_url = f"/incident_details/{incident_id}"
        comment.link_text = "ver incidente"