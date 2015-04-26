from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_403_FORBIDDEN)

from app.logging import logger
from app.views.auth.exceptions import (
    EmailAddressAlreadyUsedException,
    InvalidEmailAddressException,
    UserNotFoundException,
    InvalidPasswordException,
    LoginFailedException,
)
from app.views.exceptions import (
    ParseException,
    BadRequestException,
    ForbiddenException,
)


_CODE_TO_EXCEPTION = {
    HTTP_400_BAD_REQUEST: [
        InvalidEmailAddressException,
        ParseException,
        BadRequestException,
    ],
    HTTP_401_UNAUTHORIZED: [
        UserNotFoundException,
        InvalidPasswordException,
    ],
    HTTP_403_FORBIDDEN: [
        ForbiddenException,
    ],
    HTTP_409_CONFLICT: [
        EmailAddressAlreadyUsedException,
        LoginFailedException,
    ],
}


def _find_code_for_exception(exc):
    exc_type = type(exc)
    for code in _CODE_TO_EXCEPTION:
        if (exc_type in _CODE_TO_EXCEPTION[code]):
            return code
    return HTTP_500_INTERNAL_SERVER_ERROR


def custom_exception_handler(exc):
    logger.error('Exception caught: {}, error: {}.'.format(type(exc).__name__, exc))

    status_code = _find_code_for_exception(exc)
    response = Response(status=status_code,
                        data={
                            'detail': (hasattr(exc, 'detail') and exc.detail) or
                                      (hasattr(exc, 'message') and exc.message) or
                                      'No detail',
                            'code': (hasattr(exc, 'code')) and exc.code or 0
                        })

    return response