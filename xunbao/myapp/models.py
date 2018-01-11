from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    solved = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Problems(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100000, blank=True)
    image = models.ImageField(null=True)