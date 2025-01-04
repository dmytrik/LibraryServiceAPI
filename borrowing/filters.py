from django_filters import rest_framework as filters

from borrowing.models import Borrowing


class CustomFilter(filters.FilterSet):
    """
    FilterSet for CustomFilter
    """

    is_active = filters.BooleanFilter(
        method="filter_is_active", label="Active"
    )
    user_id = filters.NumberFilter(method="filter_user_id")

    class Meta:
        model = Borrowing
        fields = ["is_active", "user_id"]

    def filter_is_active(self, queryset, name, value):
        if value:
            return queryset.filter(actual_return_date__isnull=True)
        else:
            return queryset.filter(actual_return_date__isnull=False)

    def filter_user_id(self, queryset, name, value):
        request = self.request
        if request.user.is_staff:
            if value:
                return queryset.filter(user_id=value)
            return queryset
        else:
            return queryset.filter(user=request.user)
