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
        self.message = f"{self.cause}: {self.invalid_fields}"


class MissingFieldsException(InvalidFieldsException):
    """Raised when a query is malformed."""

    def __init__(self, missing_fields=[], **kwargs):
        super().__init__("Missing Fields", missing_fields, **kwargs)


class ExtraFieldsException(InvalidFieldsException):
    """Raised when a query is malformed."""

    def __init__(self, extra_fields=[], **kwargs):
        super().__init__("Extra Fields", extra_fields, **kwargs)


class MissingRequestParameterError(Exception):
    """Raised when a required field is missing."""

    def __init__(self, message: str = None, **kwargs):
        self.message = message
        self.kwargs = kwargs
        super().__init__(message)


class LoginValidationException(Exception):
    """Raised when login data is incorrect"""

    def __init__(self, message: str = None, **kwargs):
        self.message = message if message else "Login data is incorrect"
        self.kwargs = kwargs
        super().__init__(message)


class ObjectCreationException(Exception):
    """Raised when an object cannot be created"""

    def __init__(self, object: str, id=None, **kwargs):
        self.message = f"No se pudo crear el objeto {object}"
        self.kwargs = kwargs


class ObjectNotFoundException(Exception):
    """Raised when an object was not found"""

    def __init__(self, object: str, object_id, **kwargs):
        self.message = "No se encontró el objeto {} con identificador {}".format(
            object, object_id
        )
        self.kwargs = kwargs


class ObjectUpdateException(Exception):
    """Raised when an object cannot be created"""

    def __init__(self, object: str, **kwargs):
        self.message = "Hubo un problema con la creación del objeto {}, probablemente por un parámetro inválido".format(
            object
        )
        self.kwargs = kwargs


class IncorrectRoleException(Exception):
    """Raised when a related instance is not found"""

    def __init__(self, current_role, needed_role, **kwargs):
        self.message = "El usuario tiene rol {} y necesita ser {}".format(
            current_role, needed_role
        )


class RepeatedUniqueFieldException(Exception):
    """Raised when a related instance is not found"""

    def __init__(self, object, key, **kwargs):
        self.message = "Ya existe un objeto de tipo {} con el identificador {}".format(
            object, key
        )


class IncorrectTokenException(LoginValidationException):
    """Raised when the id in the token differs from the one in the request"""

    def __init__(self, token_id: int, request_id: int, **kwargs):
        self.message = f"El id {token_id} del token no coincide con el id {request_id} de la request"
        self.kwargs = kwargs


class AuthorizationNotPresentException(LoginValidationException):
    """Raised when the id in the token differs from the one in the request"""

    def __init__(self, **kwargs):
        self.message = (
            f"No se encontró autorización en el header o su formato es inválido"
        )
        self.kwargs = kwargs


class DependencyMismatchException(Exception):
    """Raised when there is a dependency mismatch between 2 objects"""

    def __init__(
        self, object: str, id: int, second_object: str, second_id: int, **kwargs
    ):
        self.message = "El objeto {} con id {} no pertence al objeto {} con id {}".format(
            object, id, second_object, second_id
        )
        self.kwargs = kwargs


class UpdateException(Exception):
    """Raised when there is an error with the new state of an object"""

    def __init__(self, object: str, id: int, **kwargs):
        self.message = "El objeto {} con id {} no puede actualizarse".format(object, id)
        self.kwargs = kwargs


class OrderStatusNotValidException(Exception):
    """Raised when there is an error with the update of an order status"""

    def __init__(self, current_status: str, new_status: str, **kwargs):
        self.message = f"No se puede actualizar el pedido del estado {current_status} al estado {new_status}"
        self.kwargs = kwargs
