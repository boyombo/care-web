from django.urls import path

from client import views


urlpatterns = [
    path('api_register/', views.register_api),
    path('api_login/', views.login_api),
    path('upload_photo/<int:id>/', views.upload_photo),
]
