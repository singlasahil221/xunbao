from rest_framework import serializers
from .models import Profile,Problems
from django.contrib.auth.models import User


class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ('pk','desc','image',)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name','last_name')


class LeaderboardSerializers(serializers.ModelSerializer):
	#last = serializers.SlugRelatedField(read_only=True,slug_field='last_name')
	User = UserSerializer(many=True)
	class Meta:
		model = Profile
		fields = ('User','solved')
