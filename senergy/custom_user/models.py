from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    name = models.CharField(null=False, max_length=10)
    weight = models.FloatField(null=False)
    average_sleep_time = models.FloatField(null=False)
    sleep_at = models.TimeField(null=True)
    image = models.URLField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
