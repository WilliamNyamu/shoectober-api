from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, WishlistSerializer
from .models import Product, Category, Review, Wishlist
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from .permissions import IsCreatororReadOnly, IsAuthororReadOnly, IsUserorReadOnly
from django.shortcuts import get_object_or_404

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
        # product = Product.objects.get(id = product_id) # when we use this, and the object does not exist our program will crash and return a 500 error.
        # # Use the get_object_or_404 django shortcut
        product = get_object_or_404(Product, id=product_id)
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

class WishlistListView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Wishlist.objects.filter(author = self.request.user)
        return queryset

class WishlistRetrieveView(RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Wishlist.objects.filter(author = self.request.user)
        return queryset
    
class WishListCreateView(CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id') # retrieve from the url
        # product = Product.objects.get(id=product_id) # when we use this and the object does not exist our program will crush if no object is found and return 500
        # # Use the get_object_or_404 instead
        product = get_object_or_404(Product, id=product_id)

        # Prevent duplicate wishlist entry
        if Wishlist.objects.filter(user=self.request.user, product = product).exists():
            return Response(
                {
                    'error': 'Product already in wishlist'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(product = product, user = self.request.user)
        
class WishListUpdateView(UpdateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserorReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id') # Retrieve the product id from the url
        queryset = Wishlist.objects.filter(product__id = product_id) # filter the product by the queryset. This also checks whether the user is authenticated and implements the custom permission
        return queryset

class WishListDestroyView(DestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserorReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = Wishlist.objects.filter(product__id = product_id)
        return queryset
    