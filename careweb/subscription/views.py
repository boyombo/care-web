from django.shortcuts import render, redirect
from django.contrib import messages

from client.models import Client
from subscription.forms import SubscriptionForm


def subscribe(request):
    client = Client.objects.get(user=request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            messages.success(request, "Subscription was successful")
            return redirect("profile")
    else:
        form = SubscriptionForm()
    return render(
        request, "subscription/subscribe.html", {"object": client, "form": form}
    )
