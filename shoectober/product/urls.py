from django.urls import path
from . import views

# Beware of the trailing hashes
urlpatterns = [
    path("products/create/", views.ProductCreateView.as_view(), name="create-products"),
    path("products/", views.ProductListView.as_view(), name='products'),
    path("category/", views.CategoryListView.as_view(), name="categories"),
]