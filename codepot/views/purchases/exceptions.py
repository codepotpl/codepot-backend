from codepot.exceptions import CodepotException


class PurchaseException(CodepotException):
    pass


class UserPurchaseNotFoundException(PurchaseException):
    def __init__(self, user_id):
        super().__init__('No purchase found for user with ID: {}.'.format(user_id), 300)
