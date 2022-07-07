from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import add_currency_values
from .models import Currency


@receiver(post_save, sender=Currency)
def get_new_currency_rates(sender, instance, **kwargs):
    """Runs task to add new currency rates"""

    if instance.id:
        # get new rates for all currencies
        add_currency_values.delay()
