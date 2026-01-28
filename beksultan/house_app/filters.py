from django_filters import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
             'city': ['exact'],
             'region': ['exact'],
             'district': ['exact'],
             'rooms': ['exact'],
             'floor': ['exact'],
             'condition': ['exact'],
             'property_type': ['exact'],
            'price':['gt', 'lt']
        }