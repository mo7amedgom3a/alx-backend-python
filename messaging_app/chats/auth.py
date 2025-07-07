"""
Authentication utilities for the chats application.
"""
from rest_framework import serializers, status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that adds user information to the token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra response data
        data['user_id'] = str(self.user.user_id)
        data['username'] = self.user.username
        data['email'] = self.user.email
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses the custom token serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user.
    
    Args:
        user: User instance
        
    Returns:
        dict: Token data including refresh and access tokens
    """
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': str(user.user_id),
        'username': user.username,
    }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    
    def validate(self, data):
        """
        Validate that password and password_confirm match.
        """
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def validate_email(self, value):
        """
        Validate email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        # Remove password_confirm from the data
        validated_data.pop('password_confirm')
        
        # Create the user
        user = User.objects.create_user(**validated_data)
        return user


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token for the new user
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return Response({
            "user": serializer.data,
            "tokens": tokens,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)
