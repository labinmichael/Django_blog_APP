from rest_framework import serializers
from django.contrib.auth.models import User
# Creating tokens manually
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name  = serializers.CharField()
    username   = serializers.CharField()
    password   = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate(self, data):
        data = super().validate(data)
        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name =validated_data["first_name"],
            last_name =validated_data["last_name"],
            username =validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class Loginserializer(serializers.Serializer):
    username   = serializers.CharField()
    password   = serializers.CharField()

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Account not found')
        return value
        

    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        
        if not user:
            return {'message': 'Invalid credentials', 'data': 'N/A'}
        
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        
        return {
            'message': 'Login success',
            'data': {
                'token': {
                    'refresh': str(refresh_token),
                    'access': str(access_token),
                }
            }
        }
