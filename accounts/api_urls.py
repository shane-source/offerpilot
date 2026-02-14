from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import RegisterView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="api-register"),
    path("login/", LoginView.as_view(), name="api-login"),
    path("refresh/", TokenRefreshView.as_view(), name="api-refresh"),
]
