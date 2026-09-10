import requests


def get_weather_data(latitude, longitude):
    """
    Fetch live weather data from Open-Meteo API.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,"
        "rain,wind_speed_10m,surface_pressure"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data.get("current", {})

        weather_data = {
            "temperature": current.get("temperature_2m", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "rainfall": current.get("rain", 0),
            "wind_speed": current.get("wind_speed_10m", 0),
            "pressure": current.get("surface_pressure", 0),
        }

        return weather_data

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }