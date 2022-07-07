import hashlib

from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings

from .helpers import get_currency_values
from .models import Currency, CurrencyRate


@shared_task(name="add_currency_values")
def add_currency_values():
    """Gets currency rates from the 3rd party service and add them to the
    database."""

    # get a list of currency codes
    currencies = Currency.objects.all()
    if not currencies:
        return

    # get rate values from the third party service
    rate_values = get_currency_values()
    if not rate_values:
        return

    # prepare the data
    new_rate_values = []
    added_rates = CurrencyRate.objects.all().values_list("hash", flat=True)
    for currency in currencies:
        if currency.code not in rate_values["Valute"]:
            continue

        hash = hashlib.sha256(f"{currency.code} {rate_values['Date']}".encode(
            "utf-8")).hexdigest()
        if hash in added_rates:
            continue

        new_rate_values.append(
            CurrencyRate(
                currency=currency,
                value=rate_values["Valute"][currency.code]["Value"],
                value_date=rate_values["Date"],
                nominal=rate_values["Valute"][currency.code]["Nominal"],
                hash=hash
            )
        )

    if new_rate_values:
        # NOTE: add new rate values
        CurrencyRate.objects.bulk_create(new_rate_values)


@shared_task(name="delete_old_currency_values")
def delete_old_currency_values():
    """Deletes currency rates with an expired date."""

    today = datetime.today().replace(hour=0, minute=0, second=0)
    expired_date = today - timedelta(
        days=settings.CURRENCY_VALUE_STORAGE_PERIOD)
    CurrencyRate.objects.filter(value_date__lt=expired_date).delete()
