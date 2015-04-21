from app import CodepotException


class AuthException(CodepotException):
    pass


class EmailAddressAlreadyUsedException(AuthException):
    def __init__(self):
        super().__init__('Email address already taken.', 100)


class InvalidEmailAddressException(AuthException):
    def __init__(self):
        super().__init__('Email address is not valid', 101)