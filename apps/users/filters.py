from django_filters.rest_framework import FilterSet, DateFilter


# Create your filters here.


class DailyActivityFilterSet(FilterSet):

    from_date = DateFilter(field_name="date", lookup_expr="gte")
    to_date = DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        fields = ("date",)