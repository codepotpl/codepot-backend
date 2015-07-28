from rest_framework.exceptions import (
    NotAuthenticated,
    AuthenticationFailed,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_410_GONE,
)
from jsonschema.exceptions import ValidationError as JSONValidationError

from codepot.exceptions import (
    RegistrationClosedException,
    TicketsLimitExceededException,
)
from codepot.logging import logger
from codepot.views.auth.exceptions import (
    EmailAddressAlreadyUsedException,
    InvalidEmailAddressException,
    UserNotFoundException,
    InvalidPasswordException,
    LoginFailedException,
    InvalidUserIdException,
)
from codepot.views.exceptions import (
    ParseException,
    BadRequestException,
    ForbiddenException,
)
from codepot.views.promo_codes.exceptions import PromoCodeNotFoundException
from codepot.views.purchases.exceptions import (
    UserPurchaseNotFoundException,
    PromoCodeForPurchaseNotFoundException,
    PromoCodeForPurchaseNotActiveException,
    PromoCodeForPurchaseHasExceededUsageLimit,
    UserAlreadyHasPurchaseException,
    ProductNotFoundException,
    ProductInactiveException,
    InvalidPaymentInfoException,
)
from codepot.views.workshops.exceptions import (
  IllegalWorkshopAttendee,
  WorkshopNotFoundException,
  WorkshopIllegalAccessException,
  WorkshopMessageNotFoundException,
  WorkshopWithoutPurchaseSignAttemptException,
  UserAlreadySignedForWorkshopException,
  MentorCannotSignForOwnWorkshopException,
  WorkshopMaxAttendeesLimitExceededException,
  UserAlreadySignedForWorkshopInTierException,
)

_CODE_TO_EXCEPTION = {
    HTTP_400_BAD_REQUEST: [
        InvalidEmailAddressException,
        ParseException,
        BadRequestException,
        JSONValidationError,
    ],
    HTTP_401_UNAUTHORIZED: [
        UserNotFoundException,
        InvalidPasswordException,
        NotAuthenticated,
        AuthenticationFailed,
    ],
    HTTP_403_FORBIDDEN: [
        ForbiddenException,
        InvalidUserIdException,
      WorkshopIllegalAccessException,
    ],
    HTTP_404_NOT_FOUND: [
        PromoCodeNotFoundException,
        UserPurchaseNotFoundException,
      WorkshopNotFoundException,
      WorkshopMessageNotFoundException,
    ],
    HTTP_409_CONFLICT: [
        EmailAddressAlreadyUsedException,
        LoginFailedException,
        PromoCodeForPurchaseNotFoundException,
        PromoCodeForPurchaseNotActiveException,
        PromoCodeForPurchaseHasExceededUsageLimit,
        UserAlreadyHasPurchaseException,
        ProductNotFoundException,
        ProductInactiveException,
        InvalidPaymentInfoException,
        IllegalWorkshopAttendee,
        WorkshopWithoutPurchaseSignAttemptException,
      UserAlreadySignedForWorkshopException,
      MentorCannotSignForOwnWorkshopException,
      WorkshopMaxAttendeesLimitExceededException,
        UserAlreadySignedForWorkshopInTierException,
    ],
    HTTP_410_GONE: [
        RegistrationClosedException,
        TicketsLimitExceededException,
    ]
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