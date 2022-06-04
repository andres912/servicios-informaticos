from datetime import datetime
from http import HTTPStatus
import os

from flask import jsonify
from project.models.exceptions import DependencyMismatchException, ExtraFieldsException, IncorrectRoleException, InvalidItemVersionsException, LoginValidationException, MissingFieldsException, ObjectCreationException, ObjectNotFoundException, ObjectUpdateException, RepeatedUniqueFieldException

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
    def verify_fields(cls, request_json, request_body, optional_fields=set()):
        request_keys = set(request_json.keys())
        fields_to_check = request_body - optional_fields
        if cls.is_testing():
                cls.convert_dates(request_json)
        if request_keys == fields_to_check:
            return  # everything is ok
        missing_fields = fields_to_check - request_keys
        if missing_fields:
            raise MissingFieldsException(missing_fields=missing_fields)
        extra_fields = request_keys - fields_to_check.union(optional_fields)
        if extra_fields:
            raise ExtraFieldsException(extra_fields=extra_fields)



    @classmethod
    def convert_dates(cls, request_json):
        for key in request_json.keys():
            if "_date" in key:
                request_json[key] = DateHelper.get_date_from_string(request_json[key])

class ErrorHandler:
    @classmethod
    def determine_http_status(cls, exception):
        if isinstance(exception, ExtraFieldsException):
            return HTTPStatus.BAD_REQUEST
        if isinstance(exception, LoginValidationException):
            return HTTPStatus.UNAUTHORIZED
        if isinstance(exception, ObjectNotFoundException):
            return HTTPStatus.NOT_FOUND
        if isinstance(exception, ObjectCreationException):
            return HTTPStatus.BAD_REQUEST
        if isinstance(exception, ObjectUpdateException):
            return HTTPStatus.BAD_REQUEST
        if isinstance(exception, IncorrectRoleException):
            return HTTPStatus.FORBIDDEN
        if isinstance(exception, RepeatedUniqueFieldException):
            return HTTPStatus.CONFLICT
        if isinstance(exception, DependencyMismatchException):
            return HTTPStatus.CONFLICT
        if isinstance(exception, InvalidItemVersionsException):
            return HTTPStatus.UNPROCESSABLE_ENTITY
        return HTTPStatus.INTERNAL_SERVER_ERROR

    @classmethod
    def determine_http_error_response(cls, exception):
        http_response = cls.determine_http_status(exception)
        error_message = (
            exception.message
            if http_response != HTTPStatus.INTERNAL_SERVER_ERROR
            else "Internal server error"
        )
        return jsonify({"error": error_message}), http_response


