from django.urls import path

from client import views


urlpatterns = [
    path('register', views.register),
]
