from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    """
        Serializer for the Book model with validation for inventory and daily_fee.
    """

    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee",)

    def validate(self, data):
        if data['inventory'] < 0:
            raise serializers.ValidationError({"inventory": "Inventory cannot be negative."})

        if data['daily_fee'] <= 0:
            raise serializers.ValidationError({"daily_fee": "Daily fee must be greater than zero."})

        return data
