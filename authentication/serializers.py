from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'profile_image']

    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
        )
        if profile_image:
            user.profile_image = profile_image
            user.save()
        return user

# User detail/update serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'is_active', 'is_staff',
            'profile_image', 'last_login', 'created_at'
        ]
        read_only_fields = ['id', 'role', 'is_active', 'is_staff', 'last_login', 'created_at']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}