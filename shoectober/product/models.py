from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    creator = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="product_image/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name="product_reviews", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="author_reviews", on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(blank=True, null=True) #using positive small integer field saves database space
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} reviewed {self.product}"
    

class Wishlist(models.Model):
    product = models.ForeignKey(Product, related_name="wishlist_product", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_wishlist", on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Super-enforcing duplicate prevention checks
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_wishlist_item')
        ]

    def __str__(self):
        return f"{self.user} added {self.product} to wishlist"


class Purchase(models.Model):
    product = models.ForeignKey(Product, related_name="purchases", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="purchases", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} purchased {self.quantity}x {self.product}"
    