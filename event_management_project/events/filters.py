import django_filters
from .models import Event, Category

class EventFilter(django_filters.FilterSet):
    # Search/Filter by Title and Location (Case-insensitive contains)
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category__name',
        to_field_name='name',
        lookup_expr='exact'
    )
    # Filter by Date Range (Stretch Goal)
    date_range_start = django_filters.DateTimeFilter(field_name='date_and_time', lookup_expr='gte')
    date_range_end = django_filters.DateTimeFilter(field_name='date_and_time', lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['title', 'location', 'category', 'date_and_time']