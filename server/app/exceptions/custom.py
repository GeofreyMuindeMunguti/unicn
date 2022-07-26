from fastapi import HTTPException


class InvalidDateFormat(Exception):

    def __init__(self, message: str) -> None:
        self.message = message


# The detail attribute is a temporary fix for backward compatibility of the apps.
class HttpErrorException(HTTPException):
    def __init__(self, status_code: int, error_code: str, error_message: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.detail = error_message


class DaoException(Exception):

    def __init__(self, resource: str, message: str) -> None:
        self.resource = resource
        self.message = message


class InvalidStateException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
