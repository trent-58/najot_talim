from django_filters import rest_framework as filters
from .models import Car


class CarFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name="brand", lookup_expr="icontains")
    model = filters.CharFilter(field_name="model", lookup_expr="icontains")
    year_min = filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="year", lookup_expr="lte")
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    color = filters.CharFilter(field_name="color", lookup_expr="icontains")

    class Meta:
        model = Car
        fields = [
            "brand",
            "model",
            "year_min",
            "year_max",
            "price_min",
            "price_max",
            "color",
        ]
