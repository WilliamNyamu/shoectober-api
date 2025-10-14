from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .models import Product, Category, Review
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from .permissions import IsCreatororReadOnly, IsAuthororReadOnly

# Create your views here.
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

# Product model views
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductRetrieveView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatororReadOnly]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response['message'] = 'Product updated successfully'
        return response

class ProductDestroyView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatororReadOnly]


class ReviewListView(ListAPIView):
    """List reviews for a specific product"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Fetch the variable in the url
        product_id =self.kwargs.get('product_id') # self.kwargs is a dictionary that captures the variables in the url
        # then match the filter it properly
        queryset = Review.objects.filter(product__id = product_id)
        return queryset
    
class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id = product_id)
        serializer.save(product = product, author = self.request.user)

class ReviewUpdateView(UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthororReadOnly]

    # First of all give the required reviews for the specific post
    # Then as the urlpattern lengthens, it will retrieve the specific review instance to update
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = Review.objects.filter(product__id = product_id)
        return queryset

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response['message'] = 'Review update successful'
        return response

class ReviewDestroyView(DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthororReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = Review.objects.filter(product__id = product_id)
        return queryset
    