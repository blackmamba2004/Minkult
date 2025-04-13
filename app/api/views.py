from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    rest_framework as filters,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from park.models import Park
from .serializers import ParkSerializer


class ParkFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", required=False)
    category = CharFilter(field_name="category", lookup_expr="icontains", required=False)
    description = CharFilter(field_name="description", lookup_expr="icontains", required=False)
    status = CharFilter(field_name="status", lookup_expr="icontains", required=False)
    full_address = CharFilter(field_name="full_address", lookup_expr="icontains", required=False)
    street = CharFilter(field_name="street", lookup_expr="icontains", required=False)

    lat_from = NumberFilter(field_name="lat", lookup_expr="gte", required=False)
    lat_to = NumberFilter(field_name="lat", lookup_expr="lte", required=False)
    lon_from = NumberFilter(field_name="lon", lookup_expr="gte", required=False)
    lon_to = NumberFilter(field_name="lon", lookup_expr="lte", required=False)

    class Meta:
        model = Park
        fields = [
            "name",
            "category",
            "status",
            "full_address",
            "street",
            "lat_from",
            "lat_to",
            "lon_from",
            "lon_to",
        ]


class ParkPagination(PageNumberPagination):
    page_size_query_param = "size"
    max_page_size = 30


# class ParkViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Park.objects.all().order_by("id")
#     serializer_class = ParkSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = ParkFilter
#     pagination_class = ParkPagination


class ParkViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с парковыми данными.
    Используется для получения списка парков.
    """
    queryset = Park.objects.all()
    serializer_class = ParkSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ParkFilter
    pagination_class = ParkPagination

    # Описание метода для отображения списка парков
    @swagger_auto_schema(
        operation_description="Получить список всех парков с фильтрацией",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Имя парка", type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY, description="Категория парка", type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_QUERY, description="Статус парка", type=openapi.TYPE_STRING),
            openapi.Parameter('full_address', openapi.IN_QUERY, description="Полный адрес парка", type=openapi.TYPE_STRING),
            openapi.Parameter('street', openapi.IN_QUERY, description="Улица парка", type=openapi.TYPE_STRING),
            openapi.Parameter('lat_from', openapi.IN_QUERY, description="Минимальная широта", type=openapi.TYPE_NUMBER),
            openapi.Parameter('lat_to', openapi.IN_QUERY, description="Максимальная широта", type=openapi.TYPE_NUMBER),
            openapi.Parameter('lon_from', openapi.IN_QUERY, description="Минимальная долгота", type=openapi.TYPE_NUMBER),
            openapi.Parameter('lon_to', openapi.IN_QUERY, description="Максимальная долгота", type=openapi.TYPE_NUMBER),
            openapi.Parameter('size', openapi.IN_QUERY, description="Размер страницы", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request):
        """
        Получить список всех парков с возможностью фильтрации.
        """
        # Применение фильтров
        queryset = Park.objects.all()
        filterset = ParkFilter(request.query_params, queryset=queryset)

        # Применение пагинации
        paginator = ParkPagination()
        result_page = paginator.paginate_queryset(filterset.qs, request)
        serializer = ParkSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)