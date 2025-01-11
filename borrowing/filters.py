from django_filters import rest_framework as filters

from borrowing.models import Borrowing


class CustomFilter(filters.FilterSet):
    """
    FilterSet for CustomFilter
    """

    is_active = filters.BooleanFilter(
        method="filter_is_active", label="Active"
    )
    user_id = filters.NumberFilter(method="filter_by_user_id")

    class Meta:
        model = Borrowing
        fields = ["is_active", "user_id"]

    def filter_is_active(self, queryset, value):
        if value is True:
            return queryset.filter(actual_return_date__isnull=True)
        elif value is False:
            return queryset.filter(actual_return_date__isnull=False)
        return queryset

    def filter_by_user_id(self, queryset, value):
        if self.request.user.is_staff:
            if value:
                return queryset.filter(user_id=value)
            return queryset

        return queryset.filter(user=self.request.user)
