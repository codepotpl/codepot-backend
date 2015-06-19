from django.test import TestCase

from codepot.models.promo_codes import PromoCode


class PromoCodeTests(TestCase):
    def test_if_promo_code_is_deactivated_automatically_when_usage_limit_is_zero(self):
        promo_code = PromoCode.objects.create(usage_limit=1, active=True)

        self.assertTrue(promo_code.active)
        self.assertEqual(promo_code.usage_limit, 1)

        promo_code.usage_limit -= 1

        promo_code.save()

        self.assertFalse(promo_code.active)
        self.assertEqual(promo_code.usage_limit, 0)
