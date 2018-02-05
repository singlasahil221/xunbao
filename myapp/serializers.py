from rest_framework import serializers
from .models import Profile,Problems
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ('desc','image',)



class LeaderboardSerializers(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(read_only=True,slug_field='username')	
	class Meta:
		model = Profile
		fields = ('user','solved')
