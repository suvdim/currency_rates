from rest_framework import viewsets
from django_filters import rest_framework as filters

from .models import Currency, CurrencyRate
from .serializers import CurrencySerializer, CurrencyRateSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by("title")
    serializer_class = CurrencySerializer


class CurrencyRateListView(viewsets.ModelViewSet):
    queryset = CurrencyRate.objects.all().order_by("-value_date")
    serializer_class = CurrencyRateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("currency", "value_date")

    def get_queryset(self):
        currencies = self.request.query_params.get("currency_code_latest__in")
        if currencies is not None:
            # get only latest currency rates
            return CurrencyRate.objects.filter(
                currency__code__in=currencies.replace(" ", "").split(
                    ",")).order_by("currency", "-value_date").distinct(
                "currency")

        return super().get_queryset()
