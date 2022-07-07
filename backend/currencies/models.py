import hashlib

from django.db import models


class Currency(models.Model):
    title = models.CharField("Title", max_length=255)
    code = models.CharField("Code", max_length=5)

    class Meta:
        verbose_name = "currency"
        verbose_name_plural = "currencies"

    def __str__(self):
        return self.title


class CurrencyRate(models.Model):
    currency = models.ForeignKey(
        Currency,
        verbose_name="Currency",
        related_name="related_currency",
        on_delete=models.CASCADE
    )
    value = models.DecimalField("Value", max_digits=8, decimal_places=4)
    value_date = models.DateTimeField("Value Date")
    nominal = models.IntegerField("Nominal", default=1)
    hash = models.CharField(max_length=64, unique=True, null=True, default=None)

    class Meta:
        verbose_name = "currency rate"
        verbose_name_plural = "currency rates"
        ordering = ("-value_date",)

    def __str__(self):
        return self.currency.title

    def save(self, *args, **kwargs):
        if self.hash is None:
            self.hash = hashlib.sha256(
                f"{self.currency.code} {self.value_date}".encode(
                    "utf-8")).hexdigest()
        super().save(*args, **kwargs)
