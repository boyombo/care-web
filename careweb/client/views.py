from pprint import pprint

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
#from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
#from django.urls import reverse_lazy

from client.models import Client, Dependant
from client.forms import RegForm, LoginForm, PersonalInfoForm, \
    AssociationsForm, DependantForm, PhotoForm

import logging
logger = logging.getLogger(__name__)


@login_required
def profile(request, pk=None):
    if pk:
        client = Client.objects.get(pk=pk)
    else:
        client = Client.objects.get(user=request.user)
    return render(request, 'client/profile.html', {'profile': client})


def register(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password']
            username = form.cleaned_data['email']

            new_user = User.objects.create_user(
                username=username,
                password=pwd
            )

            client = form.save(commit=False)
            client.user = new_user
            client.email = username
            client.save()
            _user = authenticate(username=username, password=pwd)
            if _user:
                login(request, _user)
                return redirect('profile', pk=client.id)
            else:
                return redirect('login')
    else:
        form = RegForm()
    return render(request, 'client/register.html', {"form": form})


def client_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #import pdb;pdb.set_trace()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            cl = Client.objects.get(user=request.user)
            return redirect('profile', pk=cl.id)
    else:
        form = LoginForm()
    return render(request, 'client/login.html', {'form': form})


class ClientView(UpdateView):
    model = Client


class PlanView(ClientView):
    fields = ['package_option', 'payment_option', 'payment_instrument']
    template_name = 'client/plan.html'


class PersonalInfoView(ClientView):
    form_class = PersonalInfoForm
    template_name = 'client/personal.html'


class ContactView(ClientView):
    fields = ['phone_no', 'whatsapp_no', 'home_address']
    template_name = 'client/contact.html'


class WorkView(ClientView):
    fields = ['occupation', 'company', 'office_address']
    template_name = 'client/work.html'


class PCPView(ClientView):
    fields = ['pcp']
    template_name = 'client/pcp.html'


class AssociationsView(ClientView):
    template_name = 'client/associations.html'
    form_class = AssociationsForm


def dependants(request, pk):
    client = Client.objects.get(pk=pk)
    _deps = Dependant.objects.filter(primary=client)
    return render(
        request,
        'client/dependants.html',
        {
            'object': client,
            'dependants': _deps
        }
    )


def add_dependant(request):
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        form = DependantForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.primary = client
            obj.save()
            messages.info(request, 'Dependant added successfully')
            return redirect('profile_dependants', pk=client.id)
    else:
        form = DependantForm()
    return render(
        request,
        'client/add_dependant.html',
        {
            'form': form,
            'object': client
        }
    )


## Endpoints

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = RegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usr = User.objects.create_user(
                username=email, password=password, email=email)
            obj = form.save(commit=False)
            obj.user = usr
            obj.save()
            return JsonResponse(
                {
                    'success': True,
                    'client': {
                        'id': obj.id,
                        'surname': obj.surname,
                        'firstName': obj.first_name,
                        'email': obj.email,
                        'phone': obj.phone_no,
                        'photo': ''
                    }
                }
            )
    return JsonResponse({'success': False})


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        logger.info('logging in...')
        form = LoginForm(request.POST)
        logger.info('form {}'.format(form.data))
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logger.info('form {}'.format(form.cleaned_data))

            usr = authenticate(username=username, password=password)
            if usr is not None:
                try:
                    client = Client.objects.get(user=usr)
                except Client.DoesNotExist:
                    return JsonResponse(
                        {
                            'error': 'Please contact support, your account is not configured correctly',
                            'success': False
                        }
                    )
                else:
                    host = 'https://{}'.format(request.get_host())
                    if client.photo:
                        photo_url = '{}{}'.format(host, client.photo.url)
                    else:
                        photo_url = ''
                    return JsonResponse(
                        {
                            'client': {
                                'id': client.id,
                                'surname': client.surname,
                                'firstName': client.first_name,
                                'phone': client.phone_no,
                                'email': client.email,
                                'photo': photo_url
                            },
                            'success': True
                        }
                    )


@csrf_exempt
def upload_photo(request, id):
    cl = get_object_or_404(Client, pk=id)
    #import pdb;pdb.set_trace()
    pprint('got client')
    pprint(cl)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=cl)
        pprint(form)
        if form.is_valid():
            form.save()
            host = 'https://{}'.format(request.get_host())
            if cl.photo:
                photo_url = '{}{}'.format(host, cl.photo.url)
            else:
                photo_url = ''
    return JsonResponse(
        {
            'client': {
                'id': cl.id,
                'surname': cl.surname,
                'firstName': cl.first_name,
                'phone': cl.phone_no,
                'email': cl.email,
                'photo': photo_url
            },
            'success': True
        }
    )
