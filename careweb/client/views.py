from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from client.forms import RegForm, LoginForm
from client.models import Client


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
                        'email': obj.email
                    }
                }
            )
    return JsonResponse({'success': False})


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
                    return JsonResponse(
                        {
                            'client': {
                                'id': client.id,
                                'surname': client.surname,
                                'firstName': client.first_name,
                                'phone': client.phone_no,
                                'email': client.email
                            },
                            'success': True
                        }
                    )
