from django.conf.urls import (
    patterns,
    url)

from codepot.views import (
    auth as auth_views,
    purchases as purchases_views,
    promo_codes as promo_codes_views,
    prices as prices_views,
    users as users_views,
    workshops as workshops_views,
)

auth_patterns = patterns(
    '',
    url(r'^auth/sign-in/$', auth_views.sign_in),
    url(r'^auth/sign-up/$', auth_views.sign_up),
    url(r'^auth/reset-pass/initialize/$', auth_views.reset_pass_initialize),
    url(r'^auth/reset-pass/finalize/$', auth_views.reset_pass_finalize)
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
    url(r'^prices/$', prices_views.get_prices)
)

user_patterns = patterns(
    '',
    url(r'^users/(?P<user_id>.+)/purchase/$', users_views.get_user_purchase),
    url(r'^users/(?P<user_id>.+)/workshops/$', workshops_views.list_user_workshops_or_sign_for_workshops),
    url(r'^users/(?P<user_id>.+)/workshops/(?P<workshop_id>.+)/$', workshops_views.delete_user_workshop)
)

workshops_patterns = patterns(
    '',
    url(r'^workshops/$', workshops_views.get_workshops),
    url(r'^workshops/search/$', workshops_views.search_workshops),
    url(r'^workshops/(?P<workshop_id>.+)/attendees/$', workshops_views.get_workshop_attendees)
)

workshops_messages_patterns = patterns(
  '',
  url(r'^workshops/(?P<workshop_id>.+)/messages/$', workshops_views.list_or_create_workshop_message),
  url(r'^workshops/(?P<workshop_id>.+)/messages/(?P<message_id>.+)/$', workshops_views.delete_workshop_message)
)

urlpatterns = \
    auth_patterns + \
    purchase_patterns + \
    promo_codes_patterns + \
    tickets_patterns + \
    user_patterns + \
    workshops_patterns + \
    workshops_messages_patterns
