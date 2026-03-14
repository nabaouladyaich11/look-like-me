from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]