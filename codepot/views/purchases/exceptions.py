from codepot.exceptions import CodepotException


class PurchaseException(CodepotException):
    pass


class UserPurchaseNotFoundException(PurchaseException):
    def __init__(self, user_id):
        super().__init__('No purchase found for user with ID: {}.'.format(user_id), 300)


class PromoCodeForPurchaseNotFoundException(PurchaseException):
    def __init__(seld, code):
        super().__init__('Given promo code: {}, does not exist.'.format(code), 301)


class PromoCodeForPurchaseNotActiveException(PurchaseException):
    def __init__(seld, code):
        super().__init__('Given promo code: {} is not active'.format(code), 302)


class PromoCodeForPurchaseHasExceededUsageLimit(PurchaseException):
    def __init__(seld, code):
        super().__init__('Given promo code: {} has exceeded usage limit'.format(code), 303)


class UserAlreadyHasPurchaseException(PurchaseException):
    def __init__(seld, user_id, purchase_id):
        super().__init__('User: {} already has purchase: {}'.format(user_id, purchase_id), 304)
