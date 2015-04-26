from app import CodepotException


class BadRequestException(CodepotException):
    pass


class ForbiddenException(CodepotException):
    pass

