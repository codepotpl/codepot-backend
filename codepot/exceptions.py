from codepot.logging import logger


class CodepotException(Exception):
    def __init__(self, detail=None, code=0):
        self.detail = detail or 'No details'
        self.code = code


class RegistrationClosedException(CodepotException):
    def __init__(self):
        super().__init__('Registration closed', 400)


class TicketsLimitExceededException(CodepotException):
    def __init__(self):
        super().__init__('Tickets limit exceeded', 401)


def log_and_raise(message, exc_class):
    logger.error(message)
    raise exc_class(message)

