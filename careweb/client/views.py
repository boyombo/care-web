from pprint import pprint

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from client.forms import RegForm, LoginForm, PhotoForm
from client.models import Client

import logging
logger = logging.getLogger(__name__)


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
