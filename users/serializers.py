from rest_framework import serializers
from .models import UserModel


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('email', 'password')
        

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class ConfirmPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=6)
