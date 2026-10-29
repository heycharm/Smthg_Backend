import requests

ELEXON_BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets"


def get_wind_actuals():
    url = f"{ELEXON_BASE_URL}/FUELHH/stream"

    params = {
        "publishDateTimeFrom": "2026-01-01T00:00:00Z",
        "publishDateTimeTo": "2026-02-01T00:00:00Z",
        "fuelType": "WIND",
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def get_wind_forecasts():
    url = f"{ELEXON_BASE_URL}/WINDFOR/stream"

    params = {
        "publishDateTimeFrom": "2026-01-01T00:00:00Z",
        "publishDateTimeTo": "2026-02-01T00:00:00Z",
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()
