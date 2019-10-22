from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from client.models import Dependant, Client
from client.forms import RegisterForm


def profile(request):
    profile = Client.objects.all()
    context = {"profile": profile}
    return render(request, 'client/profile.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['pwd1']
            username = form.cleaned_data['username']
            client = form.save(commit=False)

            new_user = User.objects.create_user(
                username=username,
                password=pwd
            )
            client.user = new_user
            client.email = username
            client.save()
            _user = authenticate(username=username, password=pwd)
            if _user:
                login(request, _user)
                return redirect('profile')
            else:
                return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'client/register.html', {"form": form})
