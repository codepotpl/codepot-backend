from codepot.exceptions import CodepotException


class BadRequestException(CodepotException):
    pass


class ParseException(BadRequestException):
    pass


class ForbiddenException(CodepotException):
    pass
