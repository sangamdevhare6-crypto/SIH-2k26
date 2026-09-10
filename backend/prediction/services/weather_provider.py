from .openmeteo_service import get_openmeteo_weather
from .imd_service import get_imd_current_weather

from prediction.data_fusion import normalize_weather_data


def get_weather(latitude, longitude):

    """
    Unified weather provider.

    Priority:
    1. IMD
    2. Open-Meteo fallback
    """

    # ======================================
    # TRY IMD
    # ======================================

    imd_response = get_imd_current_weather()

    if imd_response.get("status") == "success":

        imd_data = imd_response.get("data")

        # Future:
        # Find nearest IMD weather station
        # and normalize its data.

        if imd_data:

            # IMD data mapping will be added
            # after API access is available.
            pass

    # ======================================
    # OPEN-METEO FALLBACK
    # ======================================

    weather = get_openmeteo_weather(
        latitude,
        longitude
    )

    # Normalize all weather sou
    weather = normalize_weather_data(
        weather,
        source="OPEN_METEO"
    )

    return weather