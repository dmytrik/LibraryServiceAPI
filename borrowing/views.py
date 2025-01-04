import datetime

from django.http import HttpResponseRedirect
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from borrowing.filters import CustomFilter
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingReturnBookSerializer
)
from payment.models import Payment
from payment.service import create_stripe_session



class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for borrowing related objects.
    Provides actions: list, create, retrieve.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomFilter

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")
        if self.request.user.is_staff:
            return queryset.order_by("actual_return_date")
        return queryset.filter(user=self.request.user).order_by("actual_return_date")

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action == "return_book":
            return BorrowingReturnBookSerializer

        return BorrowingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data["book"]

        expected_return_date = serializer.validated_data["expected_return_date"]

        if datetime.date.today() > expected_return_date:
            raise ValidationError("No valid expected return date")

        if book.inventory <= 0:
            raise ValidationError("No copies available in inventory.")

        book.inventory -= 1
        book.save()

        borrowing = serializer.save(user=self.request.user)

        create_stripe_session(borrowing, request)

        payment = Payment.objects.get(borrowing=borrowing)

        return HttpResponseRedirect(payment.session_url, status=status.HTTP_302_FOUND)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
        permission_classes=[IsAuthenticated],
    )
    def return_book(self, request, pk=None):
        """
        Additional post action to return a book.
        """
        with transaction.atomic():
            borrowing = self.get_object()

            if borrowing.actual_return_date:
                raise ValidationError("This borrowing has already been returned.")

            borrowing.actual_return_date = datetime.date.today()
            borrowing.save()


            book = borrowing.book
            book.inventory += 1
            book.save()

            response = create_stripe_session(borrowing, request)

            if response:
                return HttpResponseRedirect("/api/borrowings/", status=status.HTTP_302_FOUND)

            payment = Payment.objects.filter(type="FINE", borrowing=borrowing)[0]

            return HttpResponseRedirect(payment.session_url, status=status.HTTP_302_FOUND)
