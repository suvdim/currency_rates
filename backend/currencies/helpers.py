import requests
from django.conf import settings


def get_currency_values():
    """Returns currencies values."""

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    try:
        response = requests.get(settings.CURRENCY_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()

        return None
    except requests.exceptions.RequestException:
        # TODO: print error
        return None
