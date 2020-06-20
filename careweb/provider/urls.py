from django.urls import path
from provider import views

urlpatterns = [
    path('profile', views.profile, name='provider_profile'),
    path('change-password', views.change_default_password, name='provider_change_password'),
    path('view-client', views.view_client, name='provider_view_client'),
    path('client-detail/<str:code>/<str:client_type>/<str:cid>', views.view_client_detail, name='provider_client_detail'),
]
