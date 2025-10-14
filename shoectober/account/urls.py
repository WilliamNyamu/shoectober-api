from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.login_view, name="login"),

    path("api-auth/", include('rest_framework.urls')),
]