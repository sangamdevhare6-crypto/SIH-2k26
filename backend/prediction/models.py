from django.db import models


class WeatherRecord(models.Model):
    location = models.CharField(max_length=150)

    latitude = models.FloatField()
    longitude = models.FloatField()

    rainfall = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    source = models.CharField(
        max_length=50,
        default="open-meteo"
    )

    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.recorded_at}"


class PredictionRecord(models.Model):

    RISK_CHOICES = [
        ("LOW", "Low"),
        ("MODERATE", "Moderate"),
        ("HIGH", "High"),
        ("EXTREME", "Extreme"),
    ]

    weather_record = models.ForeignKey(
        WeatherRecord,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weather_record.location} - {self.risk_level}"



class MonitoringLocation(models.Model):
    name = models.CharField(max_length=150, unique=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Alert(models.Model):

    ALERT_LEVELS = [
        ("HIGH", "High"),
        ("EXTREME", "Extreme"),
    ]

    location = models.CharField(max_length=150)

    risk_level = models.CharField(
        max_length=20,
        choices=ALERT_LEVELS
    )

    message = models.TextField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.risk_level}"


