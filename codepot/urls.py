from django.conf.urls import (
    patterns,
    url,
)

from codepot.views import (
    auth as auth_views,
    purchases as purchases_views,
)

auth_patterns = patterns(
    '',
    url(r'^auth/sign-in/$', auth_views.sign_in),
    url(r'^auth/sign-up/$', auth_views.sign_up),
)

purchase_patterns = patterns(
    '',
    url(r'^purchases/$', purchases_views.handle_purchase)
)

urlpatterns = auth_patterns + purchase_patterns
