from django.urls import path

from subscription import views

urlpatterns = [
    path("new/", views.NewSubscriptionView.as_view(), name="subscription_new"),
    path("bank/", views.bank, name="subscription_bank"),
    path("card/", views.card_subscription, name="subscription_card"),

    # APIs
    path("payment/", views.CreateSubscriptionPayment.as_view(), name="subscription_payment"),
]
