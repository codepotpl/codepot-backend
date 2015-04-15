from django.contrib.auth.models import User
from django.db import models

from rest_framework import serializers


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'first_name',
            'last_name',
        )

    def get_id(self, obj):
        return obj.user.id