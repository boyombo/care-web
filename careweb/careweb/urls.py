"""careweb URL Configuration
"""
# from django.contrib import admin
from baton.autodiscover import admin
from django.conf import settings

# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from core import views as core_views

urlpatterns = [
    path("client/", include("client.urls")),
    path("payment/", include("payment.urls")),
    path("subscription/", include("subscription.urls")),
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("agent_app_login/", core_views.login_agent),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("forgot-pwd/", core_views.forgot),
    path("change-pwd/", core_views.change_pwd),
    path("change-password/", core_views.change_pwd_web, name="change_password"),
    path(
        "post-register/",
        TemplateView.as_view(template_name="post_register.html"),
        name="post_register",
    )
    # path('profile', TemplateView.as_view(template_name='base.html'), name='profile'),
    # path('register', TemplateView.as_view(template_name='base.html'), name='register'),
]


urlpatterns += [
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path(
        "accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
    ),
    path(
        "accounts/password-reset/",
        core_views.forgot,
        # auth_views.PasswordResetView.as_view(from_email="noreply@futurecare.ng"),
        name="password-reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uid>/<token>/",
        core_views.reset_confirm,
        # auth_views.PasswordResetConfirmView.as_view(post_reset_login=True),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

admin.site.site_header = "Futurecare"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
