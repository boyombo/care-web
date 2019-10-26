from django.urls import path

from client import views


urlpatterns = [
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.client_login, name='login'),

    path('plan/<int:pk>/', views.PlanView.as_view(), name='profile_plan'),
    path('personal/<int:pk>/', views.PersonalInfoView.as_view(),
         name='profile_personal'),
    path('contact/<int:pk>/', views.ContactView.as_view(),
         name='profile_contact'),
    path('work/<int:pk>/', views.WorkView.as_view(), name='profile_work'),
]
