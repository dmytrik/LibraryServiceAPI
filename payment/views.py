from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import stripe

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
)


stripe.api_key = settings.STRIPE_SECRET_KEY


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


class PaymentSuccessView(APIView):
    """
    View for handling successful payment responses from Stripe.

    This view processes the successful payment callback from Stripe, updates the
    payment status to 'PAID', and returns the payment details including the
    amount paid and the currency.

    Methods:
        get: Handles the GET request for successful payment. Updates the payment status
             and returns the payment details.
    """

    def get(self, request, *args, **kwargs):

        try:
            payment_id = request.query_params.get("payment_id")
            payment = get_object_or_404(Payment, id=int(payment_id))
            session = stripe.checkout.Session.retrieve(payment.session_id)

            if payment.status != "PAID":
                payment.status = "PAID"
                payment.save()

            return Response(
                {
                    "message": "Payment successful",
                    "amount_paid": session.amount_total / 100,
                    "currency": session.currency,
                },
                status=status.HTTP_200_OK,
            )

        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class PaymentCancelView(APIView):
    """
    View for handling cancelled payment responses from Stripe.

    This view processes the cancelled payment callback from Stripe, updates the
    payment status to 'PENDING', and provides a link to the Stripe session
    for the user to retry the payment.

    Methods:
        get: Handles the GET request for a cancelled payment. Updates the payment
             status and returns a message indicating cancellation and a link for
             retrying the payment.
    """

    def get(self, request, *args, **kwargs):
        try:
            payment_id = request.query_params.get("payment_id")
            payment = get_object_or_404(Payment, id=int(payment_id))
            session = stripe.checkout.Session.retrieve(payment.session_id)

            if payment.status != "PENDING":
                payment.status = "PENDING"
                payment.save()

            return Response(
                {
                    "message": "Payment was cancelled.You can pay the rent within 24 hours",
                    "pay": session.url,
                    "amount_paid": session.amount_total / 100,
                    "currency": session.currency,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
