from django.contrib import admin
from .models import WeatherRecord, PredictionRecord
from .models import WeatherRecord, PredictionRecord, MonitoringLocation, Alert

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = (
        "location",
        "rainfall",
        "temperature",
        "humidity",
        "recorded_at"
    )

    list_filter = ("location", "recorded_at")
    search_fields = ("location",)


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "weather_record",
        "risk_level",
        "created_at"
    )

    list_filter = ("risk_level", "created_at")


@admin.register(MonitoringLocation)
class MonitoringLocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "latitude",
        "longitude",
        "is_active",
        "created_at"
    )

    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    list_display = (
        "location",
        "risk_level",
        "is_active",
        "created_at"
    )

    list_filter = (
        "risk_level",
        "is_active",
        "created_at"
    )

    search_fields = ("location",)