from rest_framework import viewsets, mixins

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer
)


class PaymentListCreateView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    def get_queryset(self):
        queryset = Payment.objects.select_related("borrowing")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(borrowing__user__id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer
