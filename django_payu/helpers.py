from django.conf import settings
from django.http.response import JsonResponse
from django.utils.datetime_safe import strftime
from django.utils.timezone import now

from codepot.logging import logger


class BadRequestJsonResponse(JsonResponse):
    status_code = 400


class DjangoPayException(Exception):
    def __init__(self, message):
        self.message = message


class NoParamException(DjangoPayException):
    pass


class BadParamValueException(DjangoPayException):
    pass


class PaymentStatus:
    STATUS_NEW = "new"
    STATUS_STARTED = "started"
    STATUS_FAILED = "failed"
    STATUS_COMPLETED = "completed"


class ErrorMessages():
    NOT_VALID_IP_ADDRESS = "not valid IP address"
    NOT_VALID_EMAIL_ADDRESS = "not valid email address"
    NOT_VALID_QUANTITY = "not valid quantity"
    NOT_VALID_UNIT_PRICE = "not valid unit price"

    PAYMENT_NOT_FOUND = "payment not found"
    ORDER_ID_NOT_FOUND = "orderId not found"
    STATUS_NOT_FOUND = "status not found"
    EXT_ORDER_ID_NOT_FOUND = "extOrderId not found"
    BAD_JSON_STRUCTURE = "bad JSON structure"
    QUANTITY_NOT_FOUND = "quantity not found"
    QUANTITY_MALFORMED = "quantity malformed"
    USER_NOT_FOUND = "user not found"
    USER_ID_NOT_FOUND = "user_id not found"
    TITLE_NOT_FOUND = "title not found"
    PRICE_NOT_FOUND = "price not found"
    PRICE_MALFORMED = "price malformed"
    EMPTY_JSON_RESPONSE = "empty JSON"
    EMPTY_REQUEST_RESPONSE = "empty request"
    NOT_A_JSON_RESPONSE = "not a JSON"
    NOT_AJAX_REQUEST = "not ajax request"


class Logger():
    @staticmethod
    def i(msg):
        logger.info(msg)

    @staticmethod
    def e(msg):
        logger.error(msg)

    @staticmethod
    def __log(msg, tag):
        if hasattr(settings, "DJANGO_PAYU_LOG_FILE") and settings.DJANGO_PAYU_LOG_FILE:
            log_file = open(settings.DJANGO_PAYU_LOG_FILE, "a")
            log_msg = "{}\t{}\t{}\n".format(
                strftime(now(), "%Y-%m-%d %H:%M:%S"),
                tag,
                msg,

            )
            log_file.write(log_msg)
            log_file.close()
