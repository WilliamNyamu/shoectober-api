from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name']
    
class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'token']

    def validate(self, attrs):
        """Confirm that both password fields match"""
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        """Create a user instance upon registration"""
        validated_data.pop('password2')
        # Create a user
        user = User.objects.create_user(**validated_data) # pass in the validated data; will match in the respective fields
        # Create a token for the user
        Token.objects.create(user=user)

        return user
    
    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user = obj)
        return token.key

    
