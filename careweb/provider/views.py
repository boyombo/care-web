from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from client.forms import ChangePasswordForm
from client.models import Client, Dependant
from provider.forms import ProviderCommentForm
from provider.models import CareProvider, ProviderComment


@login_required
def profile(request):
    provider = CareProvider.objects.get(email=request.user.username)
    if provider.uses_default_password:
        messages.warning(request, 'You need to change your password to proceed')
        return HttpResponseRedirect(reverse('provider_change_password'))
    return render(request, 'provider/profile.html', {'profile': provider})


@login_required
def change_default_password(request):
    form = ChangePasswordForm
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("new_password")
            user = request.user
            user.set_password(password)
            user.is_active = True
            user.save()
            provider = CareProvider.objects.get(email=user.username)
            provider.uses_default_password = False
            provider.save()
            messages.success(
                request,
                "Your password was changed successfully. You can now login with your new password",
            )
            logout(request)
            return HttpResponseRedirect(reverse("login"))
        messages.error(request, "One or more field empty")
    return render(request, "registration/change_default_password.html", {"form": form})


@login_required
def view_client(request):
    code = request.GET.get('code')
    if code:
        clients = Client.objects.filter(
            Q(lashma_no__iexact=code) | Q(lashma_quality_life_no__iexact=code) | Q(email__iexact=code) | Q(
                phone_no=code))
        if not clients.exists():
            messages.error(request, "Client with supplied detail not found")
            return HttpResponseRedirect(reverse('provider_profile'))
        if clients.count() > 1:
            messages.warning(request, "Detail matched more than one client. Provide LASHMA Code or Quality Life number")
            return HttpResponseRedirect(reverse('provider_profile'))
        client = clients.first()
        return render(request, 'provider/client_profile.html', {'client': client, 'code': code})
    messages.error(request, "Client detail required")
    return HttpResponseRedirect(reverse('provider_profile'))


@login_required
@permission_required('provider.is_provider')
def view_client_detail(request, code, client_type, cid):
    if client_type not in ['principal', 'dependant']:
        messages.error(request, "Invalid client type")
        return HttpResponseRedirect(reverse('provider_view_client') + f"?code={code}")
    provider = CareProvider.objects.get(email=request.user.username)
    client = None
    reports = None
    if client_type == 'principal':
        if not Client.objects.filter(id=cid).exists():
            messages.error(request, "Invalid principal ID")
            return HttpResponseRedirect(reverse('provider_view_client') + f"?code={code}")
        client = Client.objects.get(id=cid)
        reports = ProviderComment.objects.filter(provider=provider, client=client)
    elif client_type == 'dependant':
        if not Dependant.objects.filter(id=cid).exists():
            messages.error(request, "Invalid dependant ID")
            return HttpResponseRedirect(reverse('provider_view_client') + f"?code={code}")
        client = Dependant.objects.get(id=cid)
        reports = ProviderComment.objects.filter(provider=provider, dependant=client)
    if not client:
        messages.error(request, "Invalid request")
        return HttpResponseRedirect(reverse('provider_view_client') + f"?code={code}")
    form = ProviderCommentForm
    if request.method == 'POST':
        form = ProviderCommentForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.provider = provider
            if client_type == 'principal':
                f.client = client
            else:
                f.dependant = client
                f.client = client.primary
            f.save()
            messages.success(request, "Comment saved successfully")
            return HttpResponseRedirect(
                reverse('provider_client_detail', kwargs={'code': code, 'client_type': client_type, 'cid': cid}))
        else:
            messages.error(request, "Both doctor and comment field must be filled")
    return render(request, "provider/client_detail.html",
                  {
                      'client_type': client_type,
                      'code': code,
                      'client': client,
                      'reports': reports,
                      'form': form
                  })
