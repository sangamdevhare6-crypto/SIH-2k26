def normalize_weather_data(data, source="UNKNOWN"):
    """
    Convert weather data from different APIs
    into one standard format.
    """

    return {
        "rainfall": float(data.get("rainfall", 0) or 0),

        "temperature": float(
            data.get("temperature", 0) or 0
        ),

        "humidity": float(
            data.get("humidity", 0) or 0
        ),

        "wind_speed": float(
            data.get("wind_speed", 0) or 0
        ),

        "pressure": float(
            data.get("pressure", 0) or 0
        ),

        "source": data.get("source", source)
    }