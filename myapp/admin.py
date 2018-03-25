from django.contrib import admin
from . models import Profile, Problems, logs

# Register your models here.
admin.site.register(Profile)
admin.site.register(Problems)
admin.site.register(logs)