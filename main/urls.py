from django.conf.urls import (
    include,
    url,
    patterns,
)
from django.contrib import admin
from codepot.views import payments as payments_views

admin_patterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

api_patterns = patterns(
    '',
    url(r'^api/', include('codepot.urls', namespace='codepot')),
)

django_payu_patterns = patterns(
    '',
    url(r'^django_payu/', include('django_payu.urls')),
    url(r'^payments/payment_completed$', payments_views.handle_payment, name='django_pay_complete'),
)

urlpatterns = admin_patterns + api_patterns + django_payu_patterns
