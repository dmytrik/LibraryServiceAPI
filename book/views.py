from rest_framework import viewsets

from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
        ViewSet for handling CRUD operations on the Book model.
        Provides standard actions like list, create, retrieve, update, and delete.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
