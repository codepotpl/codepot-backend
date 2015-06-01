from django.conf.urls import (
    patterns,
    url)

from codepot.views import (
    auth as auth_views,
    purchases as purchases_views,
    promo_codes as promo_codes_views,
    tickets as tickets_views,
    users as users_views,
)

auth_patterns = patterns(
    '',
    url(r'^auth/sign-in/$', auth_views.sign_in),
    url(r'^auth/sign-up/$', auth_views.sign_up),
)

purchase_patterns = patterns(
    '',
    url(r'^purchases/new/$', purchases_views.handle_new_purchase)
)

promo_codes_patterns = patterns(
    '',
    url(r'^promo-codes/(?P<promo_code_id>.+)/$', promo_codes_views.get_promo_code_for_id)
)

tickets_patterns = patterns(
    '',
    url(r'^tickets/prices/$', tickets_views.get_tickets_prices)
)

user_patterns = patterns(
    '',
    url(r'^users/(?P<user_id>.+)/purchase/$', users_views.get_user_purchases)
)

urlpatterns = \
    auth_patterns + \
    purchase_patterns + \
    promo_codes_patterns + \
    tickets_patterns + \
    user_patterns
