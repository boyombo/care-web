from django.urls import path

from ranger import views


urlpatterns = [
    path('profile/', views.Ranger.as_view(), name='signup')



]
