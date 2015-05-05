from django.conf.urls import (
    include,
    url,
    patterns,
)
from django.contrib import admin

admin_patterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

api_patterns = patterns(
    '',
    url(r'^api/', include('codepot.urls', namespace='peercisely')),
)
urlpatterns = admin_patterns + api_patterns
