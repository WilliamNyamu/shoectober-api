from django.urls import path, include
from . import views

# Beware of the trailing hashes
urlpatterns = [
    # Product CRUD urlpatterns
    path("products/", views.ProductListView.as_view(), name='products'),
    path("products/<int:pk>/", views.ProductRetrieveView.as_view(), name="product-retrieve"),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.ProductDestroyView.as_view(), name="product-delete"),

    # Category urlpatterns
    path("category/", views.CategoryListView.as_view(), name="categories"),

    # Review CRUD urlpatterns
    path("products/<int:product_id>/reviews/", views.ReviewListView.as_view(), name="reviews"),
    path("products/<int:product_id>/reviews/create/", views.ReviewCreateView.as_view(), name="create-review"),
    path("products/<int:product_id>/reviews/<int:pk>/update/", views.ReviewUpdateView.as_view(), name="update-review"),
    path("products/<int:product_id>/reviews/<int:pk>/delete/", views.ReviewDestroyView.as_view(), name="delete-review")
]