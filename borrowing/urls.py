from rest_framework import routers

from borrowing.views import BorrowingViewSet


router = routers.DefaultRouter()
router.register("", BorrowingViewSet, basename="borrowings")

urlpatterns = router.urls

app_name = "borrowing"
