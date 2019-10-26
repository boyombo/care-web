"""careweb URL Configuration
"""
#from django.contrib import admin
from baton.autodiscover import admin
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from core import views as core_views

urlpatterns = [
    path('client/', include('client.urls')),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('agent_app_login/', core_views.login_agent),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    #path('profile', TemplateView.as_view(template_name='base.html'), name='profile'),
    #path('register', TemplateView.as_view(template_name='base.html'), name='register'),
]


urlpatterns += [
    #path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

admin.site.site_header = 'Futurecare'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
