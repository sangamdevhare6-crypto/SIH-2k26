import os
import requests


IMD_BASE_URL = "https://api.imd.gov.in/api/v1"

IMD_API_KEY = os.getenv("IMD_API_KEY", "")
IMD_API_TOKEN = os.getenv("IMD_API_TOKEN", "")
IMD_ENABLED = os.getenv(
    "IMD_ENABLED",
    "False"
).lower() == "true"


def get_imd_current_weather():

    """
    Fetch current weather data from IMD.

    Returns IMD data only when official API
    access has been configured.
    """

    if not IMD_ENABLED:

        return {
            "status": "disabled",
            "source": "IMD",
            "message": "IMD API access is not configured"
        }

    try:

        url = f"{IMD_BASE_URL}/current_wx"

        headers = {}

        if IMD_API_KEY:
            headers["x-api-key"] = IMD_API_KEY

        if IMD_API_TOKEN:
            headers["Authorization"] = (
                f"Bearer {IMD_API_TOKEN}"
            )

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        return {
            "status": "success",
            "source": "IMD",
            "data": response.json()
        }

    except requests.exceptions.HTTPError as e:

        return {
            "status": "error",
            "source": "IMD",
            "error": f"HTTP Error: {str(e)}"
        }

    except Exception as e:

        return {
            "status": "error",
            "source": "IMD",
            "error": str(e)
        }