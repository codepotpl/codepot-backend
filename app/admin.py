from django.contrib import admin

from app.models import UserProfile


@admin.register(UserProfile)
class UserProfessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
    )