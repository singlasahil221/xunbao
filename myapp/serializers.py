from rest_framework import serializers
from .models import Profile,Problems
from django.contrib.auth.models import User


class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ('val','desc','image',)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name','last_name','username')


class LeaderboardSerializers(serializers.ModelSerializer):
	user = UserSerializer(read_only = True)
	class Meta:
		model = Profile
		fields = ('user','solved')
