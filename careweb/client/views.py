from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponseRedirect
import client.forms as cf

class Client(View):
    form_class = cf.ClientForm
    template_name = 'form_client.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            client_form = form.save(commit=False)
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first name')
            
            return HttpResponseRedirect('/success/')


class Insurance(View):
    form_class = cf.InsuranceForm
    template_name = 'form_insurance.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
