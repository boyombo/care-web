from django.urls import path

from client import views


urlpatterns = [
    path("profile/<str:pk>/", views.profile, name="profile"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.client_login, name="login"),
    path("plan/<str:pk>/", views.PlanView.as_view(), name="profile_plan"),
    path(
        "personal/<str:pk>/", views.PersonalInfoView.as_view(), name="profile_personal"
    ),
    path("contact/<str:pk>/", views.ContactView.as_view(), name="profile_contact"),
    path("work/<str:pk>/", views.WorkView.as_view(), name="profile_work"),
    path("pcp/<str:pk>/", views.PCPView.as_view(), name="profile_pcp"),
    # path('associations/<int:pk>/', views.AssociationsView.as_view(),
    #     name='profile_associations'),
    path("associations/<str:pk>/", views.associations, name="profile_associations"),
    path("dependants/<str:pk>/", views.dependants, name="profile_dependants"),
    path("add_dependant/", views.add_dependant, name="profile_add_dependant"),
    path("api_register/", views.register_api),
    path("api_login/", views.login_api),
    path("upload_photo/<str:id>/", views.upload_photo),
    path("client_photo/<str:id>/", views.get_client_photo),
    path("verify/", views.verify_code),
    path("payment/", views.payment, name="paygate_card"),
    path("get_ranger_clients/<int:id>/", views.get_clients),
]
