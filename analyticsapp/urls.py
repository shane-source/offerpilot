from django.urls import path
from .views import analytics_page

urlpatterns = [
    path("analytics/", analytics_page),
]
