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
        fields = ('email',)


class LeaderboardSerializers(serializers.ModelSerializer):
	first = serializers.SlugRelatedField(read_only=True,slug_field='first_name')
	last = serializers.SlugRelatedField(read_only=True,slug_field='last_name')
	name = first+last
	class Meta:
		model = Profile
		fields = ('name','solved')
