from django.urls import path
from . import views

urlpatterns = [
    path("predict/", views.predict_rainfall, name="predict"),
    path("auto-predict/", views.auto_predict, name="auto_predict"),
]