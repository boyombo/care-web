from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from core.forms import LoginForm
from ranger.models import Ranger
from provider.models import CareProvider
from location.models import LGA
from client.models import Client


@csrf_exempt
def login_agent(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usr = authenticate(username=username, password=password)
            if usr is not None:
                try:
                    agent = Ranger.objects.get(user=usr)
                except Ranger.DoesNotExist:
                    return JsonResponse(
                        {
                            'error': 'The user is not an ranger',
                            'success': False
                        }
                    )
                else:
                    providers = [
                        {
                            'id': prov.id,
                            'name': prov.name,
                            'address': prov.address,
                            'phone1': prov.phone1,
                            'phone2': prov.phone2,
                            'lga_name': prov.lga.name,
                            'lga_id': prov.lga.id,
                        } for prov in CareProvider.objects.all()
                    ]
                    lgas = [
                        {
                            'id': lga.id,
                            'name': lga.name
                        } for lga in LGA.objects.all()
                    ]
                    clients = [
                        {
                            'id': client.id,
                            'surname': client.surname,
                            'first_name': client.first_name,
                            'middle_name': client.middle_name,
                            'phone_no': client.phone_no,
                            'whatsapp_no': client.whatsapp_no,
                            'email': client.email,
                        } for client in Client.objects.filter(ranger=agent)
                    ]

                    return JsonResponse(
                        {
                            'success': True,
                            'ranger': {
                                'first_name': agent.first_name,
                                'last_name': agent.last_name,
                                'phone': agent.phone,
                                'lga_name': agent.lga.name,
                                'lga_id': agent.lga.id,
                            },
                            'providers': providers,
                            'lgas': lgas,
                            'clients': clients
                        }
                    )
        return JsonResponse(
            {
                'error': 'Wrong credentials',
                'success': False
            }
        )
    return JsonResponse(
        {
            'error': 'Bad Request',
            'success': False
        }
    )
