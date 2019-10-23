from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from client.forms import RegForm


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usr = User.objects.create_user(
                username=email, password=password, email=email)
            obj = form.save(commit=False)
            obj.user = usr
            obj.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
