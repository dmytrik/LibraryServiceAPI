from rest_framework import serializers

from book.models import Book
from book.serializers import BookSerializer
from borrowing.models import Borrowing
from payment.models import Payment


class BorrowingSerializer(serializers.ModelSerializer):
    """
    Borrowing Serializer with validation for only one active borrowing.
    """
    book = serializers.SlugRelatedField(
        queryset=Book.objects.all(),
        slug_field="title"
    )

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "expected_return_date",
            "book"
        ]

    def validate(self, attrs):
        user = self.context["request"].user
        active_borrowings = Borrowing.objects.filter(
            user=user,
            actual_return_date__isnull=True
        )

        if active_borrowings.exists():
            raise serializers.ValidationError(
                "You already have an active borrowing. "
                "Please return the current book before borrowing another."
            )
        return attrs


class BorrowingReturnBookSerializer(serializers.ModelSerializer):
    """
        Borrowing Serializer for returning a borrowing book.
    """
    return_book = serializers.BooleanField()

    class Meta:
        model = Borrowing
        fields = ["return_book"]


class PaymentInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "money_to_pay",
        )
        read_only_fields = fields


class BorrowingListSerializer(serializers.ModelSerializer):
    """
    Borrowing Serializer for borrowing list.
    """
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    payments = PaymentInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "payments"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.actual_return_date:
            representation.pop("actual_return_date", None)
        return representation


class BorrowingDetailSerializer(serializers.ModelSerializer):
    """
    Borrowing Serializer for detail of a borrowing book.
    """
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.actual_return_date:
            representation.pop("actual_return_date", None)
        return representation
