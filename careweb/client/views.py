from django.contrib.auth.models import User
#from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
#from django.urls import reverse_lazy

from client.models import Client, Dependant
from client.forms import RegForm, LoginForm, PersonalInfoForm, \
    AssociationsForm, DependantForm


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


#def dependants(request, pk):
#    client = Client.objects.get(pk=pk)
#    DepFormset = inlineformset_factory(Client, Dependant, exclude=['primary'])
#    if request.method == 'POST':
#        formset = DepFormset(request.POST, instance=client)
#        if formset.is_valid():
#            formset.save()
#    else:
#        formset = DepFormset(instance=client)
#    return render(
#        request,
#        'client/dependants.html',
#        {
#            'formset': formset,
#            'object': client
#        })
