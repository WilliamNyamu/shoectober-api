from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, WishlistSerializer, PurchaseSerializer
from .models import Product, Category, Review, Wishlist, Purchase
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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters # for search purposes

# Create your views here.
class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Get the whole queryset or filter based on the name"""
        queryset = Category.objects.all()
        name_filter = self.request.query_params.get('name')
        if name_filter is not None:
            queryset = Category.objects.filter(name__icontains = name_filter)
        return queryset

# Product model views
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'name': ['icontains', 'iexact'],
        'category__name': ['icontains', 'iexact'], # since category is a foreign key, we use the double underscore notation to access its fields
        'price': ['lt', 'lte', 'gte']
    }
    search_fields = ['name', 'category']
    ordering_fields = ['name', 'category']
    ordering = ['name']

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['product']

    def get_queryset(self):
        queryset = Wishlist.objects.filter(user = self.request.user)
        return queryset

class WishlistRetrieveView(RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Wishlist.objects.filter(user = self.request.user)
        return queryset
    
class WishListCreateView(CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id') # retrieve from the url
        # product = Product.objects.get(id=product_id) # when we use this and the object does not exist our program will crush if no object is found and return 500
        # Use the get_object_or_404 instead
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
    

class PurchaseList(ListAPIView):
    """List the purchases made by the authenticated user"""
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Purchase.objects.filter(user = self.request.user)
        return queryset


class PurchaseCreate(CreateAPIView):
    """Making a purchase of a particular product"""
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Adding extra context so that the product can be properly validated in PurchaseSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        context['product'] = product
        return context

    # Perform create to serializer by automatically adding the product and the authenticated user
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product = product, user = self.request.user)
