from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponseRedirect
import client.forms as cf
import client.models as cm

class Ranger(View):
    form_class = cf.ClientForm
    initial = {'key': 'value'}
    template_name = 'ranger/profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'ranger/profile.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            client_form = form.save(commit=False)
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first name')
            cm.Client.objects.create()
            
            return HttpResponseRedirect('/success/')