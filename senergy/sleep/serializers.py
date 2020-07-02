from rest_framework import serializers
from sleep.models import SleepRecord


class SleepRecordSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()

    class Meta:
        model = SleepRecord
        fields = ('owner', 'id', 'date', 'sleep_at', 'hours',
                  'satisfaction_score', 'tiredness')
