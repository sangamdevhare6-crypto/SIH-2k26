from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .ml_model import predict_risk
from .weather_service import get_weather_data
from .models import WeatherRecord, PredictionRecord


@csrf_exempt
def predict_rainfall(request):

    # Only POST is allowed
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Use POST request for prediction."
        }, status=405)

    try:

        # Read JSON request
        data = json.loads(request.body)

        # Location
        location = data.get(
            "location",
            "Unknown"
        )

        # Weather inputs
        rainfall = float(
            data.get("rainfall", 0)
        )

        temperature = float(
            data.get("temperature", 0)
        )

        humidity = float(
            data.get("humidity", 0)
        )

        wind_speed = float(
            data.get("wind_speed", 0)
        )

        pressure = float(
            data.get("pressure", 1013)
        )


        # ==========================================
        # 🤖 ML MODEL PREDICTION
        # ==========================================

        risk_level = predict_risk(
            rainfall,
            temperature,
            humidity,
            wind_speed,
            pressure
        )

       # Save live weather data
        weather_record = WeatherRecord.objects.create(
            location=location,
            latitude=latitude,
            longitude=longitude,
            rainfall=weather["rainfall"],
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            wind_speed=weather["wind_speed"],
            pressure=weather["pressure"]
        )
        # Save ML prediction
        PredictionRecord.objects.create(
            weather_record=weather_record,
            risk_level=risk_level
        )

        # ==========================================
        # 🌊 INUNDATION RISK
        # ==========================================

        if risk_level == "EXTREME":

            inundation_risk = "VERY HIGH"

            warning = (
                "Extreme rainfall and severe "
                "inundation risk. Immediate action required."
            )


        elif risk_level == "HIGH":

            inundation_risk = "HIGH"

            warning = (
                "Heavy rainfall expected. "
                "Flood-prone areas should remain alert."
            )


        elif risk_level == "MODERATE":

            inundation_risk = "MODERATE"

            warning = (
                "Moderate rainfall expected. "
                "Monitor local conditions."
            )


        else:

            risk_level = "LOW"

            inundation_risk = "LOW"

            warning = (
                "Low rainfall risk. "
                "No immediate threat detected."
            )


        # ==========================================
        # 📤 API RESPONSE
        # ==========================================

        return JsonResponse({

            "status": "success",
            "record_id": weather_record.id,

            "prediction": {

                "location": location,

                "rainfall_mm": rainfall,

                "risk_level": risk_level,

                "inundation_risk": inundation_risk,

                "warning": warning
            },

            "input_data": {

                "temperature": temperature,

                "humidity": humidity,

                "wind_speed": wind_speed,

                "pressure": pressure
            }

        })


    except (
        ValueError,
        TypeError,
        json.JSONDecodeError
    ):

        return JsonResponse({

            "status": "error",

            "message": (
                "Invalid input. Please provide "
                "valid numeric values."
            )

        }, status=400)


# ==========================================
# 🏠 HOME PAGE
# ==========================================

def home(request):

    return render(
        request,
        "index.html"
    )


@csrf_exempt
def auto_predict(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        location = data.get("location", "Unknown")

        if latitude is None or longitude is None:
            return JsonResponse(
                {
                    "error": "latitude and longitude are required"
                },
                status=400
            )

        # Fetch live weather automatically
        weather = get_weather_data(latitude, longitude)

        if "error" in weather:
            return JsonResponse(
                {
                    "error": "Weather API failed",
                    "details": weather["error"]
                },
                status=500
            )

        # AI/ML Prediction
        risk_level = predict_risk(
            weather["rainfall"],
            weather["temperature"],
            weather["humidity"],
            weather["wind_speed"],
            weather["pressure"]
        )

        return JsonResponse({
            "status": "success",

            "location": location,

            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },

            "live_weather": weather,

            "prediction": {
                "risk_level": risk_level
            }
        })

    except Exception as e:

        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status=500
        )