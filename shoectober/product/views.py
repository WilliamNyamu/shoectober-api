from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')


    # Validation
    if not username or not password:
        return Response(
            {'error': "Please provide a valid username and password"},
            status= status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username = username).exists():
        return Response(
            {'error': 'username already exists! Pick another one'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists!'},
            status = status.HTTP_406_NOT_ACCEPTABLE
        )

    # After successful validation, create the user
    user = User.objects.create_user(username=username, password=password, email=email)

    #Create a token for the created user
    token = Token.objects.create(user=user)

    return Response(
        {
            'token': token.key,
            'user_id': user.id,
            'user_name': user.username,
            'message': "User created successfully"
        },
        status=status.HTTP_201_CREATED
    )
@api_view(['POST'])
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

    




# Product model views
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDestroyView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
