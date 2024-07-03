from datetime import datetime

from django.core.exceptions import FieldError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from cafe.models import Cafe, CafeLunchMenu
from cafe.permissions import IsCreatorOrReadOnly, IsAdminOrReadOnly
from cafe.serializers import CafeSerializer, CafeListSerializer, CafeDetailSerializer, CafeLunchMenuListSerializer, \
    CafeLunchMenuDetailSerializer, LunchDishSerializer


class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CafeListSerializer
        if self.action == 'retrieve':
            return CafeDetailSerializer
        return CafeSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        try:
            return [int(str_id) for str_id in qs.split(",")]
        except ValueError:
            raise ValidationError(code=400, detail="Not a valid list of IDs")

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name", None)
        address = self.request.query_params.get("address", None)
        type_ids = self.request.query_params.get("types", None)
        cuisine_ids = self.request.query_params.get("cuisines", None)
        metro_ids = self.request.query_params.get("metroes", None)
        feature_ids = self.request.query_params.get("features", None)
        ordering = self.request.query_params.get("ordering", None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if address:
            queryset = queryset.filter(address__icontains=address)
        if type_ids:
            type_ids = self._params_to_ints(type_ids)
            queryset = queryset.filter(type__in=type_ids)
        if cuisine_ids:
            cuisines = self._params_to_ints(cuisine_ids)
            queryset = queryset.filter(cuisine__in=cuisines)

        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except FieldError:
                raise ValidationError(code=400, detail="Invalid ordering")

        return queryset.distinct()


class CafeLunchMenuViewSet(viewsets.ModelViewSet):
    queryset = CafeLunchMenu.objects.all()
    serializer_class = LunchDishSerializer
    permission_classes = [IsCreatorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CafeLunchMenuDetailSerializer
        return CafeLunchMenuListSerializer

    def get_queryset(self):
        today = datetime.today().strftime("%a")
        queryset = self.queryset.filter(weekday=today)
        cafe_name = self.request.query_params.get("cafe", None)

        if cafe_name:
            queryset = queryset.filter(cafe__name__icontains=cafe_name)

        return queryset

