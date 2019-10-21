from django.urls import path

from client import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
]
