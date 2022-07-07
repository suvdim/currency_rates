from django.urls import path, include
from rest_framework import routers

from .views import CurrencyViewSet, CurrencyRateListView

router = routers.DefaultRouter()
router.register(r'currencies', CurrencyViewSet)
router.register(r'rates', CurrencyRateListView)

urlpatterns = [
    path('', include(router.urls)),
]