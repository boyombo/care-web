from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponseRedirect
import ranger.forms as rf
import ranger.models as rm
import client.models as cm

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = rf.RangerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = rf.RangerForm()
    return render(request, 'ranger/profile.html', {'form': form})

def login_ranger(request):
    if request.method == 'POST':
        form = rf.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
    else:
        form = rf.LoginForm()
    return render(request, 'ranger/login.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    if request.method == 'GET':
        profile = rm.Ranger.objects.get(user=request.user)
        context = {'profile': profile}
        return render(request, 'ranger/profile.html', context)
    else:
        # Edit profile
        profile = rm.Ranger.objects.get(user=request.user)
        form = rf.RangerForm(request.POST, instance=profile)
        form.save()
        ranger = rm.Ranger.objects.get(user=request.user)
        context = {'ranger': ranger}
        return render(request, 'ranger/profile.html', context)

def register_client(request):
    if request.method == 'POST':
        form = rf.ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client')
    else:
        form = rf.ClientForm()
    return render(request, 'ranger/client list', {'form': form})

def client_list(request):
    if request.method == 'GET':
        ranger = get_object_or_404(rm.Ranger, user=request.user)
        client = cm.Client.objects.filter(ranger=ranger)
        context = {'client': client}
        return render(request, 'ranger/client-list.html', context)



