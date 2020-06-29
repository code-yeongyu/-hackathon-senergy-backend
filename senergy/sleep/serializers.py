from rest_framework import serializers
from sleep.models import SleepRecord


class SleepRecordSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SleepRecord
        fields = (
            'owner',
            'data',
        )