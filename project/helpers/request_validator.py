from datetime import datetime
import os
from project.models.exceptions import ExtraFieldsException, MissingFieldsException, ObjectNotFoundException

class DateHelper:
    @staticmethod
    def get_date_from_string(date_string):
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
        except:
            try:
                date = datetime.strptime(date_string, "%d/%m/%Y")
            except:
                raise ValueError("Date string format not recognized")
        return date

    @staticmethod
    def get_string_from_date(date):
        return date.strftime("%d/%m/%y")


class RequestValidator:
    """
    Class that validates the request
    """

    @classmethod
    def is_testing(cls):
        return "TESTING" in os.environ and os.environ["TESTING"] == "True"
    
    @classmethod
    def verify_fields(cls, request_json, fields_to_check, optional_fields=None):
        request_keys = set(request_json.keys())
        if request_keys == fields_to_check:
            if cls.is_testing():
                cls.convert_dates(request_json)
            return
        missing_fields = fields_to_check - request_keys
        if missing_fields:
            raise MissingFieldsException(missing_fields=missing_fields)
        extra_fields = request_keys - fields_to_check
        if extra_fields:
            raise ExtraFieldsException(extra_fields=extra_fields)


    @classmethod
    def convert_dates(cls, request_json):
        for key in request_json.keys():
            if "_date" in key:
                request_json[key] = DateHelper.get_date_from_string(request_json[key])

