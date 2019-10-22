from django.urls import path

from ranger import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_ranger, name='login'),
    path('profile/', views.profile, name='profile'),

]
