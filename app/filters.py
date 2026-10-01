import django_filters
from app import models

class ScheduleFilter(django_filters.FilterSet):
    start_point = django_filters.CharFilter(field_name="route__start_point", lookup_expr="iexact")
    end_point = django_filters.CharFilter(field_name="route__end_point", lookup_expr="iexact")
    date = django_filters.DateFilter(field_name="date", lookup_expr="iexact")

    class Meta:
        model = models.Schedule
        fields = ['start_point', 'end_point', 'date']