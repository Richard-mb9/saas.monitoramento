from http import HTTPStatus


class APIError(Exception):
    """Api Error"""

    def __init__(self, status_code: HTTPStatus, message: str):
        super().__init__()
        self.status_code = status_code
        self.message = message


class BadRequestError(Exception):
    """Exception Bad Request Error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.BAD_REQUEST, message)


class ConflictError(Exception):
    """Exception Conflict Error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.CONFLICT, message)


class NotFoundError(Exception):
    """Exception Not Found Error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.NOT_FOUND, message)


class AccessDeniedError(Exception):
    """Exception Access Denied error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.FORBIDDEN, message)


class UnprocessableEntityError(Exception):
    """Exception Unprocessable Entity error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.UNPROCESSABLE_ENTITY, message)


class UnauthorizedError(Exception):
    """Exception Unauthorized error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.UNAUTHORIZED, message)


class LockedError(Exception):
    """Exception Locked error"""

    def __init__(self, message: str):
        raise APIError(HTTPStatus.LOCKED, message)
