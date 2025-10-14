from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = "category.name", read_only=True)
    creator = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'image', 'category', 'category_name', 'creator', 'created_date', 'updated_date']
        read_only_fields = ['creator','created_at', 'updated_at']
        
