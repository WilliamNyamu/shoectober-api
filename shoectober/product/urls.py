from django.urls import path, include
from . import views

# Beware of the trailing hashes
urlpatterns = [
    path("auth/signup/", views.register_view, name="signup"),
    path("auth/login/", views.login_view, name="login"),
    path("products/", views.ProductListView.as_view(), name='products'),
    path("products/<int:pk>/", views.ProductRetrieveView.as_view(), name="product-retrieve"),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.ProductDestroyView.as_view(), name="product-delete"),
    path("category/", views.CategoryListView.as_view(), name="categories"),


    path("api-auth/", include('rest_framework.urls')),
]