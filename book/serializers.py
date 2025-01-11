from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model with validation for inventory and daily_fee.
    """

    unreturned_borrowings_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
            "unreturned_borrowings_count",
        )
        read_only_field = ("id",)

    def validate(self, data):
        if data["daily_fee"] <= 0:
            raise serializers.ValidationError(
                {"daily_fee": "Daily fee must be greater than zero."}
            )

        return data

    def get_unreturned_borrowings_count(self, obj):
        return obj.borrowings.filter(actual_return_date__isnull=True).count()
