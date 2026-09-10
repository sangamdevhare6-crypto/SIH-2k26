import requests


def get_openmeteo_weather(latitude, longitude):

    try:

        url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        params = {
            "latitude": latitude,
            "longitude": longitude,

            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "surface_pressure,"
                "wind_speed_10m,"
                "rain"
            )
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current", {})

        return {
            "rainfall": float(current.get("rain", 0) or 0),

            "temperature": float(
                current.get("temperature_2m", 0) or 0
            ),

            "humidity": float(
                current.get("relative_humidity_2m", 0) or 0
            ),

            "wind_speed": float(
                current.get("wind_speed_10m", 0) or 0
            ),

            "pressure": float(
                current.get("surface_pressure", 0) or 0
            ),

            "source": "OPEN_METEO"
        }

    except Exception as e:

        return {
            "error": str(e),
            "source": "OPEN_METEO"
        }