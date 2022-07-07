from rest_framework import serializers
from .models import Currency, CurrencyRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyRateSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source="currency.code")
    currency_title = serializers.CharField(source="currency.title")

    class Meta:
        model = CurrencyRate
        fields = ["currency_code", "currency_title", "value", "value_date",
                  "nominal"]
