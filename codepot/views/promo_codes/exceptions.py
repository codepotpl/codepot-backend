from codepot.exceptions import CodepotException


class PromoCodeException(CodepotException):
    pass


class PromoCodeNotFoundException(PromoCodeException):
    def __init__(self, promo_code_id):
        super().__init__('Promo code for ID: {}, not found.'.format(promo_code_id), 200)
