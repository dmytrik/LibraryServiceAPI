from django.urls import path, include
from rest_framework import routers

from payment.views import (
    PaymentListCreateView,
    PaymentSuccessView,
    PaymentCancelView,
)


router = routers.DefaultRouter()
router.register("", PaymentListCreateView, basename="payments")

urlpatterns = [
    path("success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
    path("", include(router.urls)),
]

app_name = "payment"
