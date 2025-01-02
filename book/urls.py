from django.urls import path, include
from rest_framework import routers
from book.views import BookViewSet

app_name = "book"

router = routers.DefaultRouter()
router.register("books", BookViewSet)

urlpatterns = [path("", include(router.urls))]
