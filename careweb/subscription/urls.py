from django.urls import path

from subscription import views


urlpatterns = [
    path("new/", views.subscribe, name="subscription_new"),
]
