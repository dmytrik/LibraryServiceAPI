from rest_framework import serializers

from payment.models import Payment
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.

    This serializer handles the basic serialization and deserialization
    of Payment instances, allowing for easy conversion between complex
    Payment model instances and native Python datatypes (e.g., JSON).

    Meta:
        model (Payment): The model that this serializer is based on.
        fields (tuple): The fields to include in the serialized output.
            - id (int): Unique identifier for the payment.
            - status (str): Current status of the payment (PENDING or PAID).
            - type (str): The type of payment (PAYMENT or FINE).
            - borrowing (int): The ID of the related borrowing record.
            - session_url (str): URL to the payment session.
            - session_id (str): Payment session identifier.
            - money_to_pay (Decimal): Amount to be paid.
        read_only_fields (tuple): Fields that cannot be modified through this serializer.
            - id: The primary key is read-only and automatically generated.
    """

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )
        read_only_fields = ("id",)


class PaymentListSerializer(PaymentSerializer):
    """
    Serializer for listing Payment records.

    This serializer extends PaymentSerializer by replacing the borrowing field
    with a nested BorrowingListSerializer to provide additional details about
    the borrowing record in list views.

    Attributes:
        borrowing (BorrowingListSerializer): Provides summarized borrowing data
                                             instead of just the ID.
    """

    borrowing = BorrowingListSerializer()


class PaymentDetailSerializer(PaymentListSerializer):
    """
    Serializer for detailed view of a Payment record.

    This serializer extends PaymentListSerializer by using BorrowingDetailSerializer
    for the borrowing field, providing a more in-depth view of the related borrowing
    record.

    Attributes:
        borrowing (BorrowingDetailSerializer): Provides detailed borrowing data
                                               for a specific payment.
    """

    borrowing = BorrowingDetailSerializer()
