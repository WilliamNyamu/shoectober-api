from rest_framework import serializers
from .models import Product, Category, Review, Wishlist, Purchase

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
        # here, i got a TypeError when I didn't provide a rating, because the .get() can return None.
        rating = attrs.get('rating')

        if rating is None :
             raise serializers.ValidationError("Rating is required")
        if rating > 5 or rating == 0:
            raise serializers.ValidationError("Enter a value between 1 and 5")
        return attrs

class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    product_creator = serializers.CharField(source="product.creator", read_only=True)
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_creator', 'user', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    # Enforcing duplicate prevention checks
    def validate(self, attrs):
        # You check the user from the logged in user accessed in self.request.user using the contect
        user = self.context['request'].user
        product = attrs.get('product')

        if Wishlist.objects.filter(user = user, product = product).exists():
            raise serializers.ValidationError("Product already saved in wishlist")
        return attrs


class PurchaseSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source='category', read_only=True)
    user_name = serializers.StringRelatedField(source='user', read_only=True)
    class Meta:
        model = Purchase
        fields = ['id', 'product', 'product_name', 'user', 'user_name', 'quantity', 'paid_amount', 'purchase_date']
        read_only_fields = ['paid_amount,' 'purchase_date']
    
    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')

        if product.quantity < quantity:
            raise serializers.ValidationError(f"Only {product.quantity} is available in stock. Reduce your purchase quantity")
        return attrs
    
    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        # calculate the total amount to be paid
        total_amount = product.price * quantity
        # get the paid_amount and 
        validated_data['paid_amount'] = total_amount
        return Purchase.objects.create(**validated_data)
    

