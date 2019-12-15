from django.urls import path

from payment import views


urlpatterns = [
    path("initiate/", views.new_payment, name="initiate_payment"),
    path("paystack_callback/", views.paystack_callback),
    path("paystack_success/", views.paystack_success, name="paystack_success"),
    path("paystack_error/", views.paystack_error, name="paystack_error"),
    path("paystack_verify/", views.verify_paystack_payment),
    path("subscription_verify/", views.verify_paystack_subscription),
    path("verify_user/", views.verify_user),
    path("walkin_payment/", views.walkin_payment),
]
