from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from book.models import Book
from book.permissions import IsAdminOrReadOnly
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on the Book model.
    Provides standard actions like list, create,
    retrieve, update, and delete.
    """

    queryset = Book.objects.prefetch_related("borrowings")
    serializer_class = BookSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]

    @method_decorator(cache_page(60 * 5, key_prefix="book_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Method to dispatch the request, with caching applied
        for the crew view.

        The response is cached for 5 minutes using the
        key prefix 'book_view'.
        """
        return super().dispatch(request, *args, **kwargs)
