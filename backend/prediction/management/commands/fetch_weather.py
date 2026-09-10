from django.core.management.base import BaseCommand

from prediction.models import (
    MonitoringLocation,
    WeatherRecord,
    PredictionRecord,
    Alert
)

from prediction.services.weather_provider import get_weather
from prediction.ml_model import predict_risk


class Command(BaseCommand):

    help = "Fetch live weather data and generate AI predictions"

    def handle(self, *args, **kwargs):

        locations = MonitoringLocation.objects.filter(is_active=True)

        if not locations.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No active monitoring locations found."
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Monitoring {locations.count()} locations..."
            )
        )

        for location in locations:

            try:

                self.stdout.write(
                    f"\nFetching weather for {location.name}..."
                )

                # ==========================================
                # FETCH LIVE WEATHER DATA
                # ==========================================

                weather = get_weather(
                    location.latitude,
                    location.longitude
                )

                if "error" in weather:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Weather API Error: {weather['error']}"
                        )
                    )
                    continue

                # ==========================================
                # AI / ML PREDICTION
                # ==========================================

                risk_level = predict_risk(
                    weather["rainfall"],
                    weather["temperature"],
                    weather["humidity"],
                    weather["wind_speed"],
                    weather["pressure"]
                )

                # ==========================================
                # SAVE WEATHER RECORD
                # ==========================================

                weather_record = WeatherRecord.objects.create(
                    location=location.name,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    rainfall=weather["rainfall"],
                    temperature=weather["temperature"],
                    humidity=weather["humidity"],
                    wind_speed=weather["wind_speed"],
                    pressure=weather["pressure"],
                    source=weather.get("source", "UNKNOWN"),
                )
                
            

                # ==========================================
                # SAVE PREDICTION RECORD
                # ==========================================

                PredictionRecord.objects.create(
                    weather_record=weather_record,
                    risk_level=risk_level
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ {location.name}: {risk_level}"
                    )
                )

                # ==========================================
                # AUTOMATIC ALERT GENERATION
                # ==========================================

                if risk_level in ["HIGH", "EXTREME"]:

                    if risk_level == "HIGH":

                        message = (
                            f"Heavy rainfall warning for {location.name}. "
                            f"High flood/inundation risk detected. "
                            f"Authorities should remain prepared."
                        )

                    else:

                        message = (
                            f"EMERGENCY WARNING for {location.name}! "
                            f"Extreme rainfall and flood risk detected. "
                            f"Immediate emergency response may be required."
                        )

                    # Check existing active alert
                    existing_alert = Alert.objects.filter(
                        location=location.name,
                        risk_level=risk_level,
                        is_active=True
                    ).first()

                    # Create alert only if duplicate does not exist
                    if not existing_alert:

                        Alert.objects.create(
                            location=location.name,
                            risk_level=risk_level,
                            message=message
                        )

                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ ALERT GENERATED: "
                                f"{location.name} - {risk_level}"
                            )
                        )

                    else:

                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ Active alert already exists for "
                                f"{location.name} - {risk_level}"
                            )
                        )

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"✗ {location.name}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\nAutomatic monitoring completed successfully!"
            )
        )