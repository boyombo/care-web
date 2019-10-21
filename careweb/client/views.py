from django.shortcuts import render
from client.models import Dependant, Client


def profile(request):
    profile = Client.objects.all()
    context = {"profile": profile}
    return render(request, 'client/profile.html', context)
