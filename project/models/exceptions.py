"""Exception classes for marshmallow-related errors."""
import typing


# Key used for schema-level validation errors
SCHEMA = "_schema"


class MarshmallowError(Exception):
    """Base class for all marshmallow-related errors."""


class ValidationError(MarshmallowError):
    """Raised when validation fails on a field or schema.

    Validators and custom fields should raise this exception.

    :param message: An error message, list of error messages, or dict of
        error messages. If a dict, the keys are subitems and the values are error messages.
    :param field_name: Field name to store the error on.
        If `None`, the error is stored as schema-level error.
    :param data: Raw input data.
    :param valid_data: Valid (de)serialized data.
    """

    def __init__(
        self,
        message: typing.Union[str, typing.List, typing.Dict],
        field_name: str = SCHEMA,
        data: typing.Optional[
            typing.Union[
                typing.Mapping[str, typing.Any],
                typing.Iterable[typing.Mapping[str, typing.Any]],
            ]
        ] = None,
        valid_data: typing.Optional[
            typing.Union[
                typing.List[typing.Dict[str, typing.Any]], typing.Dict[str, typing.Any]
            ]
        ] = None,
        **kwargs,
    ):
        self.messages = [message] if isinstance(message, (str, bytes)) else message
        self.field_name = field_name
        self.data = data
        self.valid_data = valid_data
        self.kwargs = kwargs
        super().__init__(message)

    def normalized_messages(self):
        if self.field_name == SCHEMA and isinstance(self.messages, dict):
            return self.messages
        return {self.field_name: self.messages}


class BadQueryException:
    """Raised when a query is malformed."""

    def __init__(self, message: str, **kwargs):
        self.message = message
        self.kwargs = kwargs
        super().__init__(message)


class ObjectNotFoundException(Exception):
    """Raised when an object is not found in the database"""

    def __init__(self, object_name: str = None, object_id: int = None, **kwargs):
        self.message = f"Object of type '{object_name}' with id '{object_id}' not found."
        self.object_name = object_name
        self.object_id = object_id
        self.kwargs = kwargs


class InvalidFieldsException(Exception):
    """Raised when a query is malformed."""

    def __init__(self, cause, invalid_fields=[], **kwargs):
        self.kwargs = kwargs
        self.cause = cause
        self.invalid_fields = invalid_fields

class MissingFieldsException(InvalidFieldsException):
    """Raised when a query is malformed."""

    def __init__(self, missing_fields=[], **kwargs):
        super().__init__("Missing Fields", missing_fields, **kwargs)


class ExtraFieldsException(InvalidFieldsException):
    """Raised when a query is malformed."""

    def __init__(self, extra_fields=[], **kwargs):
        super().__init__("Extra Fields", extra_fields, **kwargs)

class ObjectCreationException(Exception):
    """Raised when an object could not be created"""

    def __init__(self, object, **kwargs):
        self.kwargs = kwargs
        self.object = object

