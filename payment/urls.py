from rest_framework import routers

from payment.views import PaymentListCreateView


router = routers.DefaultRouter()
router.register("", PaymentListCreateView, basename="payments")

urlpatterns = router.urls

app_name = "payment"
