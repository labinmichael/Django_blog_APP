from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username =serializers.CharField()
    password =serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']):
            raise serializers.ValidationError('username is taken')
        return data
        