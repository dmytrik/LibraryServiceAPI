from django.urls import path, include
from rest_framework import routers
from book.views import BookViewSet

app_name = "book"

router = routers.DefaultRouter()
router.register("", BookViewSet, basename="books")

urlpatterns = router.urls
