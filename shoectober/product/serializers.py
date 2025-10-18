from rest_framework import serializers
from .models import Product, Category, Review, Wishlist

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    category_name = serializers.StringRelatedField(source='category', read_only=True)
    creator = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'image', 'category', 'category_name', 'creator', 'created_date', 'updated_date']
        read_only_fields = ['creator','created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ['id', 'product', 'content', 'author', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('rating') > 5 or attrs.get('rating') == 0:
            raise serializers.ValidationError("Enter a value between 1 and 5")
        return attrs

class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'user', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    # Enforcing duplicate prevention checks
    def validate(self, attrs):
        # You check the user from the logged in user accessed in self.request.user using the contect
        user = self.context['request'].user
        product = attrs.get('product')

        if Wishlist.objects.filter(user = user, product = product).exists():
            raise serializers.ValidationError("Product already saved in wishlist")
        return attrs