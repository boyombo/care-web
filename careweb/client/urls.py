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
    path('pcp/<int:pk>/', views.PCPView.as_view(), name='profile_pcp'),
    path('associations/<int:pk>/', views.AssociationsView.as_view(),
         name='profile_associations'),
    path('dependants/<int:pk>/', views.dependants, name='profile_dependants'),
    path('add_dependant/', views.add_dependant,
         name='profile_add_dependant'),
]
