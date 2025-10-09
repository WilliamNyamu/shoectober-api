from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.register_view, name="signup"),
    path("login/", views.login_view, name="login"),

    path("api-auth/", include('rest_framework.urls')),
]