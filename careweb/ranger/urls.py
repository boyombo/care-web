from django.urls import path

from ranger import views

urlpatterns = [
    path('fund/', views.CreateFundingView.as_view(), name='fund'),
]
