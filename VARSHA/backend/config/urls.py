from django.contrib import admin
from django.urls import path, re_path
from accounts import views
from django.views.generic import TemplateView
from django.views.static import serve
from pathlib import Path

FRONTEND = Path(__file__).resolve().parent.parent.parent / 'frontend'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('signup.html', TemplateView.as_view(template_name='signup.html')),
    path('reset-password.html', TemplateView.as_view(template_name='reset-password.html')),
    path('role-login.html', TemplateView.as_view(template_name='role-login.html')),
    path('citizen-dashboard.html', TemplateView.as_view(template_name='citizen-dashboard.html')),
    path('admin-dashboard.html', TemplateView.as_view(template_name='admin-dashboard.html')),
    path('alerts-management.html', TemplateView.as_view(template_name='alerts-management.html')),
    path('reports-complaints.html', TemplateView.as_view(template_name='reports-complaints.html')),
    path('risk-map.html', TemplateView.as_view(template_name='risk-map.html')),
    path('weather-data.html', TemplateView.as_view(template_name='weather-data.html')),
    path('monitoring-stations.html', TemplateView.as_view(template_name='monitoring-stations.html')),
    path('user-management.html', TemplateView.as_view(template_name='user-management.html')),
    path('resources.html', TemplateView.as_view(template_name='resources.html')),
    path('settings.html', TemplateView.as_view(template_name='settings.html')),
    path('logs.html', TemplateView.as_view(template_name='logs.html')),
    path('profile.html', TemplateView.as_view(template_name='profile.html')),
    path('api/signup/', views.signup), path('api/login/', views.login_api),
    path('api/logout/', views.logout_api), path('api/reset-password/', views.reset_password),
    path('api/me/', views.me),
    re_path(r'^(?P<path>.*\.(?:css|js|png|jpg|jpeg|svg|ico|webp))$', serve, {'document_root': str(FRONTEND)}),
]
