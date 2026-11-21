from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    bio = serializers.CharField(source="profile.bio", read_only=True)
    class Meta:
        model = User
        fields = ["id","username","first_name","last_name","email","avatar","bio"]
    def get_avatar(self, obj):
        request = self.context.get("request")
        image = getattr(getattr(obj, "profile", None), "avatar", None)
        return request.build_absolute_uri(image.url) if image and request else (image.url if image else None)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type":"password"})
    class Meta:
        model = User
        fields = ["username","email","first_name","last_name","password"]
    def validate_username(self, value):
        if not value.strip(): raise serializers.ValidationError("Choose a username.")
        return value
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value
    def validate_password(self, value):
        validate_password(value)
        return value
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
