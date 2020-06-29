from rest_framework import serializers
from custom_user.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'weight', 'average_sleep_time', 'sleep_at', 'image', )

