from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime
from django.dispatch import receiver


class Profile(models.Model):
    user = models.ForiegnKey(User, on_delete=models.CASCADE)
    solved = models.IntegerField(default=1)
    timetaken = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-solved', 'timetaken']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Problems(models.Model):
    desc = models.CharField(max_length=100000, blank=True)
    image = models.FileField(blank=True)
    ans = models.CharField(max_length=10000, null=True)
    mydate = models.DateTimeField(default=datetime.now)
