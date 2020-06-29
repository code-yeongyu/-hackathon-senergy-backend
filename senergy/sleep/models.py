from django.db import models
from datetime import datetime


# Create your models here.
class SleepRecord(models.Model):
    owner = models.ForeignKey('auth.user',
                              related_name='sleep_owner',
                              on_delete=models.CASCADE,
                              null=False)
    datetime = models.DateTimeField(default=datetime.now)
    data = models.TextField(default='[]')