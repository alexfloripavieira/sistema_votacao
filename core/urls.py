from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('business/', include('business.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
