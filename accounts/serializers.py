# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'domain', 'owner', 'logo', 'subscription_plan', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password', 'company', 'phone', 'address', 'profile_pic', 'is_active', 'last_login_ip', 'failed_login_attempts', 'last_failed_login', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
