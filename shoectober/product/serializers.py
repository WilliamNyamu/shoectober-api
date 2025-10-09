from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = "category.name", read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image', 'category', 'category_name', 'creator']
