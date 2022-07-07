from django.contrib import admin

from .models import Currency, CurrencyRate


class CurrencyAdmin(admin.ModelAdmin):
    fields = ("title", "code")
    list_display = ["title", "code"]
    search_fields = ["title", "code"]


class CurrencyRateAdmin(admin.ModelAdmin):
    fields = ("currency", "value", "value_date", "nominal", "hash")
    list_display = ["currency", "value", "value_date", "nominal", "hash"]
    search_fields = ["currency"]


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
