from django.urls import path

from core import views

urlpatterns = [
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/reports/export/', views.export_admin_report, name='export_admin_reports'),
    path('admin/landing/', views.admin_landing_page, name='admin_landing_page'),
]
