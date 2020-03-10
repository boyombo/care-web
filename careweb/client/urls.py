from django.urls import path

from client import views

urlpatterns = [
    path("profile/<str:pk>/", views.profile, name="profile"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.client_login, name="login"),
    path("verify-account/", views.verify_code_web, name="verify_account"),
    path("change-password/", views.change_default_password, name="change_default_password"),
    path("plan/<str:pk>/", views.PlanView.as_view(), name="profile_plan"),
    # path("plan/", views.update_plan, name="profile_plan"),
    path(
        "personal/<str:pk>/", views.PersonalInfoView.as_view(), name="profile_personal"
    ),
    path("contact/<str:pk>/", views.ContactView.as_view(), name="profile_contact"),
    path("photo/<str:pk>/", views.PhotoView.as_view(), name="profile_photo"),
    path(
        "identification/<str:pk>/",
        views.IdentificationView.as_view(),
        name="profile_identification",
    ),
    path("work/<str:pk>/", views.WorkView.as_view(), name="profile_work"),
    path("pcp/<str:pk>/", views.PCPView.as_view(), name="profile_pcp"),
    # path('associations/<int:pk>/', views.AssociationsView.as_view(),
    #     name='profile_associations'),
    path("associations/<str:pk>/", views.associations, name="profile_associations"),
    path("dependants/<str:pk>/", views.dependants, name="profile_dependants"),
    path("add_dependant/", views.add_dependant, name="profile_add_dependant"),
    path(
        "remove_dependant/<str:pk>/",
        views.remove_dependant,
        name="profile_remove_dependant",
    ),
    path(
        "edit_dependant/<str:pk>/",
        views.edit_dependant,
        name="profile_edit_dependant",
    ),
    path("api_register/", views.register_api),
    # path("api_agent_register/<int:id>/", views.register_via_agent),
    path("api_agent_register/", views.CreateRangerClientView.as_view()),
    path("api_login/", views.login_api),
    path("upload_photo/<str:id>/", views.upload_photo),
    path("upload_photo_base64/<str:id>/", views.upload_photo_b64),
    path("client_photo/<str:id>/", views.get_client_photo),
    path("verify/", views.verify_code),
    path("payment/", views.payment, name="client_payment"),
    path("get_ranger_clients/<int:id>/", views.get_clients),
    path(
        "ranger_subscription/<int:client_id>/<int:ranger_id>/",
        views.create_client_subscription,
    ),
    path("info/<int:id>/", views.get_client_info),
    path("load_pcp_list/", views.load_pcp_list, name="load_pcp_list"),
    path("upload_clients/", views.upload_clients, name="upload_clients"),
    path("api_add/", views.CreateClientView.as_view(), name="api_add_client"),
    path("api_update/<str:pk>/", views.UpdateClientView.as_view(), name="api_update_client"),
    path("init/", views.GetInitialDataView.as_view(), name="init"),
    path("search/", views.SearchClientView.as_view(), name="search"),
    path("details/<int:client_id>/", views.GetClientDetail.as_view(), name="detail"),

    # AJAX Request
    path("lga/pcps", views.get_lga_pcp),
    path("pcp/get-lga", views.get_pcp_lga),
]
