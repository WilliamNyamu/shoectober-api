from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response['message'] = 'You have registered successfully'
        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check whether the user has entered the username and password
    if not username or not password:
        return Response(
            {'error': "Please provide a username and password for login"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check whether the username exists and whether the password is correct for that username
    user = authenticate(username = username, password = password) # authenticate() handles everything

    if user:
        token, created = Token.objects.get_or_create(user = user) # Retrieve the token for the user
        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'message': "Login successful :)"
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'error': "Invalid Credentials"},
            status=status.HTTP_404_NOT_FOUND
        )
