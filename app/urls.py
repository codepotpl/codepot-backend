from django.conf.urls import (
    patterns,
    url,
)

from app.views import auth_views


auth_patterns = patterns(
    '',
    url(r'^auth/sign-in/$', auth_views.sign_in),
    url(r'^auth/sign-up/$', auth_views.sign_up),
)

urlpatterns = auth_patterns