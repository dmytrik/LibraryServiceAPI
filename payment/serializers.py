from rest_framework import serializers

from payment.models import Payment
from borrowing.serializers import BorrowingListSerializer


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        )
        read_only_fields = ("id",)


class PaymentListSerializer(PaymentSerializer):
    borrowing = BorrowingListSerializer
