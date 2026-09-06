from django.contrib import admin
from django.urls import path, re_path
from accounts import views
from django.views.generic import TemplateView
from django.views.static import serve
from pathlib import Path


FRONTEND = Path(__file__).resolve().parent.parent.parent / "frontend"


urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    path("", TemplateView.as_view(
        template_name="index.html"
    ), name="home"),

    path("index.html", TemplateView.as_view(
        template_name="index.html"
    ), name="index"),

    path("signup.html", TemplateView.as_view(
        template_name="signup.html"
    ), name="signup"),

    path("reset-password.html", TemplateView.as_view(
        template_name="reset-password.html"
    ), name="reset-password"),

    path("role-login.html", TemplateView.as_view(
        template_name="role-login.html"
    ), name="role-login"),

    path("citizen-dashboard.html", TemplateView.as_view(
        template_name="citizen-dashboard.html"
    ), name="citizen-dashboard"),

    path("authority-dashboard.html", TemplateView.as_view(
        template_name="authority-dashboard.html"
    ), name="authority-dashboard"),

    path("admin-dashboard.html", TemplateView.as_view(
        template_name="admin-dashboard.html"
    ), name="admin-dashboard"),

    path("alerts-management.html", TemplateView.as_view(
        template_name="alerts-management.html"
    ), name="alerts-management"),

    path("reports-complaints.html", TemplateView.as_view(
        template_name="reports-complaints.html"
    ), name="reports-complaints"),

    path("risk-map.html", TemplateView.as_view(
        template_name="risk-map.html"
    ), name="risk-map"),

    path("weather-data.html", TemplateView.as_view(
        template_name="weather-data.html"
    ), name="weather-data"),

    path("monitoring-stations.html", TemplateView.as_view(
        template_name="monitoring-stations.html"
    ), name="monitoring-stations"),

    path("user-management.html", TemplateView.as_view(
        template_name="user-management.html"
    ), name="user-management"),

    path("resources.html", TemplateView.as_view(
        template_name="resources.html"
    ), name="resources"),

    path("settings.html", TemplateView.as_view(
        template_name="settings.html"
    ), name="settings"),

    path("logs.html", TemplateView.as_view(
        template_name="logs.html"
    ), name="logs"),

    path("profile.html", TemplateView.as_view(
        template_name="profile.html"
    ), name="profile"),


    path("api/signup/", views.signup),
    path("api/login/", views.login_api),
    path("api/logout/", views.logout_api),
    path("api/reset-password/", views.reset_password),
    path("api/me/", views.me),


    re_path(
        r"^(?P<path>.*\.(?:css|js|png|jpg|jpeg|svg|ico|webp))$",
        serve,
        {
            "document_root": str(FRONTEND)
        },
    ),
]