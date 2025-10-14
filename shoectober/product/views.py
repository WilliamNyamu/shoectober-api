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
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product model views
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductRetrieveView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDestroyView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
