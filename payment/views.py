from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
)


class PaymentListCreateView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    API view for listing and retrieving Payment records.

    This view provides endpoints for listing all payments and retrieving
    individual payment records. It supports nested borrowing data in the
    response, with different serializers based on the type of action performed
    (list or retrieve).

    Permissions:
        - Requires authentication for all actions.
        - Admin users can view all payments.
        - Regular users can only view their own payments.

    Attributes:
        permission_classes (list): Restricts access to authenticated users only.

    Methods:
        get_queryset():
            Returns the queryset of Payment objects.
            Admin users receive all payments, while regular users receive
            only payments associated with their borrowing records.

        get_serializer_class():
            Returns the appropriate serializer class based on the action being
            performed.
            - list: Uses PaymentListSerializer to provide summarized borrowing data.
            - retrieve: Uses PaymentDetailSerializer for detailed borrowing data.
            - default: Falls back to PaymentSerializer for basic CRUD operations.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the appropriate queryset for the user.

        Returns:
            QuerySet: A queryset of Payment objects. Admin users receive all
                      payments, while regular users only receive payments
                      linked to their own borrowing records.
        """
        queryset = Payment.objects.select_related("borrowing")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(borrowing__user__id=self.request.user.id)

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action.

        Returns:
            Serializer:
                - PaymentListSerializer for listing payments.
                - PaymentDetailSerializer for retrieving specific payments.
                - PaymentSerializer for other actions by default.
        """
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer
